# 附录 A　延伸阅读

这份书单按主题分组，每组挑几篇最关键的。带星号的是综述或入口性文献，适合先读。

## 连接组学

- White, J. G., Southgate, E., Thomson, J. N., & Brenner, S. (1986). The structure of the nervous system of the nematode Caenorhabditis elegans. Philosophical Transactions of the Royal Society B, 314, 1–340. 线虫连接组的原始论文，三百多页图谱，连接组学的起点。
- Scheffer, L. K., et al. (2020). A connectome and analysis of the adult Drosophila central brain. eLife, 9, e57443. 果蝇半脑的连接组，首次给出中央脑的完整连接矩阵。
- Dorkenwald, S., et al. (2024). Neuronal wiring diagram of an adult brain. Nature, 634, 124–138. FlyWire 全脑连接组的主论文，13.9 万个神经元，5000 万个突触。
- Schlegel, P., et al. (2024). Whole-brain annotation and multi-connectome cell typing of Drosophila. Nature, 634, 139–152. 与上篇配套的细胞类型注释，八千多种类型。
- MICrONS Consortium (2025). Functional connectomics spanning multiple areas of mouse visual cortex. Nature, 640, 435–447. 小鼠视觉皮层一立方毫米的结构与功能联合数据集。

## 神经元与突触

- Hodgkin, A. L., & Huxley, A. F. (1952). A quantitative description of membrane current and its application to conduction and excitation in nerve. Journal of Physiology, 117, 500–544. 动作电位的经典模型，五个方程至今仍是基准。
- Izhikevich, E. M. (2003). Simple model of spiking neurons. IEEE Transactions on Neural Networks, 14, 1569–1572. 二维模型，用四个参数复现二十多种放电模式。
- Bi, G. Q., & Poo, M. M. (1998). Synaptic modifications in cultured hippocampal neurons. Journal of Neuroscience, 18, 10464–10472. 脉冲时序依赖可塑性的原始实验。
- Eckstein, N., et al. (2024). Neurotransmitter classification from electron microscopy images at synaptic sites in Drosophila melanogaster. Cell, 187, 2574–2594. 用机器学习从电镜图像预测递质类型，FlyWire 的符号来源。

## 网络与动力学

- Brunel, N. (2000). Dynamics of sparsely connected networks of excitatory and inhibitory spiking neurons. Network, 11, 17–34. 稀疏网络的异步与同步状态分析。
- Beggs, J. M., & Plenz, D. (2003). Neuronal avalanches in neocortical circuits. Journal of Neuroscience, 23, 11167–11177. 神经雪崩与临界态的经典观察。
- Potjans, T. C., & Diesmann, M. (2014). The cell-type specific cortical microcircuit. Cerebral Cortex, 24, 785–806. 皮层柱的标准基准模型，七万七千个神经元。
- Markram, H., et al. (2015). Reconstruction and simulation of neocortical microcircuitry. Cell, 163, 456–492. 蓝脑计划的皮层柱重建。

## 全脑仿真与具身

- Shiu, P. K., et al. (2024). A Drosophila computational brain model reveals sensorimotor processing. Nature, 634, 210–219. 果蝇全脑 LIF 模型，Eon 工作的直接基础。
- Lappalainen, J. K., et al. (2024). Connectome-constrained networks predict neural activity across the fly visual system. Nature, 634, 1132–1140. 连接组约束的视觉模型。
- Wang-Chen, S., et al. (2024). NeuroMechFly v2: simulating embodied sensorimotor control in adult Drosophila. Nature Methods, 21, 2353–2362. 果蝇身体仿真框架。
- Sandberg, A., & Bostrom, N. (2008). Whole Brain Emulation: A Roadmap. Future of Humanity Institute. 全脑仿真的早期路线图，很多概念在这里被系统化。
- State of Brain Emulation Report 2025 (arXiv:2510.15745). 对 2008 年路线图的重新评估，按记录、测绘、仿真三条线梳理进展。
- Neuromorphic Simulation of Drosophila Melanogaster Brain Connectome on Loihi 2 (arXiv:2508.16792). 把 FlyWire 连接组放到 12 片神经形态芯片上运行。

## 尺度与数据

- Herculano-Houzel, S. (2009). The human brain in numbers. Frontiers in Human Neuroscience, 3, 31. 人脑细胞计数的系统综述，860 亿神经元的来源。
- Abbott, L. F., et al. (2020). The Mind of a Mouse. Cell, 182, 1372–1376. 小鼠全脑连接组的可行性与意义。

## 怎么读这些论文

如果只想了解全貌，先读 Shiu 等人的论文和 FlyWire 的主论文，再看 State of Brain Emulation Report。这三份材料能覆盖本书的大部分内容。

如果想深入方法，读 White 1986 和 Scheffer 2020，对比手工重建和自动流水线的差别，能直观感受技术进步。

如果对动力学感兴趣，从 Hodgkin-Huxley 1952 和 Brunel 2000 开始，前者是单细胞，后者是网络。两篇都不长，数学要求适中。
