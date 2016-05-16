# 大规模二分图节点影响力分析库(A Python Library for Evaluating Node Influence in Large-Scale Bipartite Graph)

## 该类库主要包括三大功能：
1. 利用桶排序（Bucket Sort）实现了对大规模图上按节点编号对图的边表进行线性复杂度的排序。
2. 在大规模二分图上高效计算出节点的近邻谱（Close Neighbor Spectrum）和谱传播功率（Spectrum Power)。
3. 可以在大规模二分图上实现SI和SIR仿真，返回某时间节点的跳数，通过比较感染不同节点的跳数来评估节点的影响力大小。

## 测试数据集
* G1 - Yahoo! Search Marketing Advertiser-Phrase Bipartite Graph, Version 1.0 (14 MB) [http://webscope.sandbox.yahoo.com/catalog.php?datatype=g]
* G3 - Yahoo! Groups User-Group Membership Bipartite Graph, version 1.0 (93 MB)[http://webscope.sandbox.yahoo.com/catalog.php?datatype=g]

### 程序清单如下：
- bucket_sort_bipartite.py
- bucket_sort_l1.py
- bucket_sort_r2.py
- gen_node_power.py
- gen_node_spectrum.py
- sir_simulation.py

