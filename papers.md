## Real-Time Intermediate Flow Estimation for Video Frame Interpolation

**keywords**：

### 引言

视频帧插值（Video Frame Interpolation，VFI）旨在在两个连续视频帧中生成中间帧，视频帧插值有许多应用如慢动作生成，视频压缩和视频帧预测。实时帧插值还可以用于高分辨率视频以减小实时视频传输带宽，为资源有限的用户提供视频剪辑服务，在显示设备上进行视频帧适应。

现实生活中由于复杂、非线性和光照改变导致视频帧插值是具有挑战性的，一些基于流的算法已经取得了显著效果。基于流的算法的常规方法包括两个步骤：（1）根据近似的光流对输入帧进行扭曲（warp），（2）使用CNN对扭曲后的帧进行融合。

光流模型并不能直接用于VFI，给定两个输入帧$I_0$和$I_1$，基于流的方法需要从我们需要生成的帧$I_t$的角度近似中间流$F_{t\to0}$和$F_{t\to1}$，但是我们需要中间流来计算中间帧$I_t$，两者之间存在冲突。许多实践通过先计算从光流模型中计算双向流，然后反向细化生成中间流。但是这样的流存在动作边界（不同帧中的物体的位置会改变）。外观流是视图合成领域的一项开创性工作，提出使用cnn从目标视图开始估计流。

这篇文章构建了一个轻量级管道，在保持直接中间流估计的简洁性，同时，实现最先进的性能。管道的主要设计理念为：

1. 不需要额外的组件，如图像深度模型，流细化模型和流反向层。
2. 端到端可学习动作估计：通过实验证明，与其引入一些不准确的运动建模，不如让CNN端到端学习中间流。
3. 为近似的中间流提供直接监督：大多数VFI模型在训练时最优最终的重建损失。直观地说，跨扭曲算子传播逐像素损失梯度对于流量估计并不有效。缺乏明确设计用于流量估计的监督会降低VFI模型的性能。

提出了IFNet，可以直接从相邻帧和时序编码输入来估计中间流。IFNet采用了从粗到细的策略，逐步提高分辨率，通过连续的IFBlock迭代更新中间流和软融合掩码。直观地，根据迭代地更新flow field，可以将对应的像素从两个输入帧移动到潜在中间帧的同一位置，使用一个混合掩码来从两个输入帧中结合像素。为了计算的高效，IFBlock只使用$3\times 3$的卷积和反卷积来构建模块。使用直接监督非常重要，当只使用最终重建损失来端到端训练IFNet，由于错误的光流估计，训练效果并不好，通过采用具有访问中间帧的教师模型来指导学生学习可以很好地改善这一情况。

结合上述设计，这篇文章提出了实时中间帧估计（Real-Time Intermediate Flow Estimation，RIFE），无需预训练模型或带光流标签的数据集即可获得令人满意的结果。这篇文章的主要贡献为：

+ 设计了一个有效的IFNet来近似中间流和引入特许蒸馏方案（即引入教师模型）来提升性能；
+ 实验表明，RIFE在几个公共基准测试中达到了SOTA性能，特别是在任意时间帧插值场景中。
+ 得益于其灵活的时间编码，RIFE可以扩展到如深度图插值和动态场景拼接等应用程序。



### 方法

#### Pipeline概述

Pipeline的整体结构如下图所示：

<img src="D:\TyporaImages\image-20231202202026662.png" alt="image-20231202202026662" style="zoom:67%;" />

给定一对连续的RGB帧$I_0$和$I_1$，目标时间帧$t(0\le t\le1)$，目标是生成中间帧${\hat I_t}$。通过输入的帧和作为额外通道输入IFNet的$t$来估计中间流$F_{t\to0}$和$F_{t\to1}$和混合映射$M$，${\hat I_t}$通过下式计算：
$$
{{\hat I}_t} = M \odot {{\hat I}_{t \leftarrow 0}} + \left( {1 - M} \right) \odot {{\hat I}_{t \leftarrow 1}}  \tag{1} 
$$

$$
{{\hat I}_{t \leftarrow 0}} = \overleftarrow W \left( {{I_0},{F_{t \to 0}}} \right),\quad {{\hat I}_{t \leftarrow 1}} = \overleftarrow W \left( {{I_1},{F_{t \to 1}}} \right) \tag{2}
$$

其中$\overleftarrow W$是图像反向扭曲（warp），$\odot$是按元素相乘，$M$是混合映射（$0\le M\le1$）。使用另一个编解码结构的CNN即RefineNet（RefineNet的结构在附录中）来细化${\hat I_t}$中的高分辨率区域，减少学生模型的工作。RefineNet最终会产生一个重建残差$\Delta(-1\le \Delta \le 1)$，我们将得到一个细化的重建图像${\hat I_t}+\Delta$。

#### 直接流估计

IFNet的工作就是通过输入的连续帧$I_0$和$I_1$和时间步$t$来估计中间流$F_{t\to0}$和$F_{t\to1}$和混合映射$M$，当$t=0$或$t=1$时，IFNet与传统的光流模型相似。IFNet的结构如下图所示：

<img src="D:\TyporaImages\image-20231202202631430.png" alt="image-20231202202631430" style="zoom:67%;" />

为了处理在中间流估计中遇到的大量动作，采用了逐渐提高分辨率的策略。具体来说，首先计算低分辨率下的流的粗略预测，这样可以认为更容易捕获大的运动，然后迭代地细化流，逐渐增加分辨率。按照这个设计，IFNet有一个堆叠的沙漏结构，其中流场通过连续的IFBlock迭代细化：
$$
\left[ \matrix{
  {F^i} \hfill \cr 
  {M^i} \hfill \cr}  \right] = \left[ \matrix{
  {F^{i - 1}} \hfill \cr 
  {M^{i - 1}} \hfill \cr}  \right] + {\rm{IF}}{{\rm{B}}^i}\left( {\left[ \matrix{
  {F^{i - 1}} \hfill \cr 
  {M^{i - 1}} \hfill \cr}  \right],t,{{\hat I}^{i - 1}}} \right) \tag{3}
$$
其中$F^{i-1}$和$M^{i-1}$表示第$i-1$个IFBlock的中间流和混合映射的当前估计。一共使用了3个IFBlock，每个有一个分辨率参数$\left( {{K^0},{K^1},{K^2}} \right) = \left( {4,2,1} \right)$，在推理时，最终的估计是$F^2$和$M^2$。对于每个IFBlock的具体结构，值得注意的是使用PReLU作为激活函数。

#### 对中间流特许蒸馏

为IFNet设计了一个特许蒸馏损失，如IFNet的结构图所示，堆叠了一个额外的IFBlock（教师模型$\text{IFB}^{Tea}$，$K^{Tea}=1$）根据目标帧$I_t^{GT}$对IFNet的结果进行细化：
$$
\left[ \matrix{
  {F^{Tea}} \hfill \cr 
  {M^{Tea}} \hfill \cr}  \right] = \left[ \matrix{
  {F^n} \hfill \cr 
  {M^n} \hfill \cr}  \right] + {\rm{IF}}{{\rm{B}}^{Tea}}\left( {\left[ \matrix{
  {F^n} \hfill \cr 
  {M^n} \hfill \cr}  \right],t,{{\hat I}^n},I_t^{GT}} \right)  \tag{4}
$$
使用$I_t^{GT}$作为特许信息，教师模型可以得到更加精确的流，定义蒸馏损失$L_{dis}$如下：
$$
{L_{dis}} = \sum\limits_{i \in \{ 0,1\} } {{{\left\| {{F_{t \to i}} - F_{t \to i}^{Tea}} \right\|}_2}}   \tag{5}
$$
这部分损失不会被反向传播到教师模型，教师模块仅在训练阶段使用，可以实现更稳定的训练和更快的收敛。

#### 实现细节

训练损失是三部分损失的组合
$$
{L_{total}} = {L_{rec}} + L_{rec}^{Tea} + {\lambda _d}{L_{dis}}  \tag{6}
$$
$\lambda_d$可以设置为0.01，重建损失的定义如下：
$$
{L_{rec}} = d\left( {{{\hat I}_t},I_t^{GT}} \right),\;L_{rec}^{Tea} = d\left( {\hat I_t^{Tea},I_t^{GT}} \right)  \tag{7}
$$
$d$是逐像素的损失，可以使用重构图像的两个拉普拉斯金字塔表示和真值之间的$L_1$损失。

**训练数据集**：Vimeo90K

**训练策略**：t=0.5，AdamW(lr=10e-4)，batch_size为64，在训练时使用余弦退火将学习率从10e-4降到10e-5。



### 结论

作者开发了一种高效灵活的VFI算法，即RIFE。使用一个独立的模块IFNet直接估计中间光流，由特许蒸馏方案监督，其中教师模型可以访问真值中间帧。实验证明，RIFE可以有效地处理不同场景的视频。此外，带有时间编码的额外输入使RIFE能够进行任意时间步长的帧插值。RIFE的轻量级特性使得下游任务更容易使用它。

