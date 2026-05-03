项目设想：Inference-Native Memory State

核心思路

在一次长工作流结束后，不再依赖“文本摘要 + 外部 embedding model”来构造记忆，而是直接利用同一次推理中已经存在的大模型上下文、权重和 KV cache，让模型生成一个极短的 memory key（例如 1–3 个词，或一小句记录文本），并在生成这些 token 的同时，保存每个 token 对应的 final-layer last-token hidden state。
最终存储的对象包括：
    •    极短文本 memory key
    •    这些 token 对应的 hidden states
    •    原始上下文文本（便于审计、人类阅读、回放）

查询时，仍然使用同一个大模型，输入类似：

“我想找……因为……请用一个词概括我想找的内容。”

然后取模型输出 token 对应的 final-layer last-token hidden state，直接与历史 memory key hidden states 做向量匹配。

这本质上是在用生成中的大模型自身充当 embedding model，但不是训练一个新 embedding 模型，而是直接利用生成时的内部状态。

⸻

研究问题

在长上下文任务中，是否可以通过保存生成型大模型在“记忆概括 token”上的 final hidden states，构建一种比“文本摘要 + embedding”更高保真的长期记忆表示，从而在较低额外计算和存储代价下，更好地支持未来的检索、召回与继续推理？

⸻

工作假设
    1.    长任务结束时，模型在生成极短概括 token 时的 final hidden states，包含了大量未被短文本摘要显式表达的上下文信息。
    2.    这种 memory state 会比传统 embedding 更贴近该模型自己的推理语义空间，因此在同模型检索下可能显著更准。
    3.    该方法无需任何额外训练；如果复用已有 KV cache，构造 memory 的边际成本很低。
    4.    由于 memory key 和 query 都由同一模型生成，它可能天然更适合捕捉该模型自己的“任务态、关注点、延续性和风格目标”。

⸻

方法边界
    •    记忆中“模型自己生成的内容”，对该次inference来说它们都只是 input。所以不能直接保存和恢复模型历史生成时未输出的完整“模型内推理”。
    •    该方法强依赖模型空间：memory key 和 query 最好由同一模型生成，因此难以直接享受未来模型升级带来的检索提升。
    •    对历史旧数据做回溯构建 memory 也可能很贵。

⸻

方法优势
    1.    不需要单独训练 embedding model 或 memory encoder。
    2.    可利用现成推理资源。在工作流结束时，如果 KV cache 仍在内存中，构造 memory 的额外成本很低。
    3.    语义对齐更强。memory key 和 query 都来自同一生成模型，理论上更贴合该模型自己的语义与推理空间。
    4.    比纯文本摘要信息密度更高。文本 key 保持可读；hidden state 保留额外上下文痕迹。

⸻

评测维度
    1.    存储成本
    •    memory key 文本大小
    •    hidden state 大小
    •    是否复用 KV cache
    •    有/无 KV cache 时的构造算力成本
    2.    检索成本
    •    query 生成 memory key 的算力
    •    向量匹配成本
    •    与传统 RAG 的总检索延迟对比
    3.    检索/问答质量
    •    recall / precision / MRR / nDCG
    •    downstream QA accuracy
    •    是否优于文本摘要 + embedding
    4.    速度
    •    memory 构造时间
    •    query 检索时间
    •    端到端任务完成时间

⸻

对照方法
    1.    本方法：memory key text + hidden state retrieval （单 memory key 和 100 个 memory key 的两个版本）
    2.    传统 RAG：文本切块 + embedding model + vector search
    3.    LLM-powered grep / tool-use retrieval /全文搜索 + LLM rerank

⸻

数据集设计
    1.    标准 benchmark
    •    现成 retrieval / long-context QA / memory benchmark
    •    用于证明方法在通用任务上的有效性
    2.    模型自生成数据集
    •    由同一模型（如 Qwen3.5-27B）生成 memory key / memory query / memory source
    •    研究问题变成：
用 Qwen3.5-27B 生成的 memory key 与 query，在 Qwen3.5-27B 自身的 hidden-state 空间里，是否比传统 embedding 检索更准确？

⸻

最小实验版本

对每个储存对象：
    1.    跑完整推理工作流，让模型生成 1/100 个概括词
    2.    保存这些 token 及其 final-layer last-token hidden states
    3.    保存原始上下文文本与引用信息

对每个查询：
    1.    让同一模型生成 1 个 query key
    2.    取对应 hidden state
    3.    做向量检索
    4.    取回候选 memory 与原文上下文
    5.    评估检索和下游回答质量

⸻

一句话概括：

这是一个利用生成型大模型自身 final hidden states 构造长期记忆的无训练方法，目标是在复用原有推理资源的前提下，获得比传统 embedding 更贴近模型内部语义空间的 memory retrieval。
