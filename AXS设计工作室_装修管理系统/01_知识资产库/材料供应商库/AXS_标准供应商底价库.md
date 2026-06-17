---
database_id: axs_material_base_01
last_updated: 2026-05-31
maintainer: AXS_System
---

# AXS 核心供应商底价库 (结构化数据)

> [!CAUTION] **数据隔离警告**
> 本库为 AXS 工作室绝密底价资产，仅限主理人与 AI 算量引擎读取。**严禁**直接将此文件暴露给客户。

## 01. 硬装与主材

```yaml
id: M_TILE_001
category: 硬装主材
brand: 诺贝尔/马可波罗同厂平替 (代工厂直发)
product: 极简微水泥/哑光素色瓷砖
spec: 750x1500mm
factory_price: 95 # 单位: 元/平米
shipping: 满1万元包上楼
lead_time: 仓储现货(3天送达)
stage: 02_泥瓦进场前3天送达
rating: 5
```

```yaml
id: M_WOOD_001
category: 定制木作
brand: 某本地头部代工厂
product: 极简隐形收纳柜/墙板/餐边柜 (ENF级)
spec: 柜体实木多层 + 肤感PET门板
factory_price: 1000 # 单位: 元/投影面积
shipping: 厂家包测量、包安装
lead_time: 定制期(35-45天)
stage: 04_油漆完工后进场
rating: 4
```

```yaml
id: M_DOOR_001
category: 硬装主材
brand: 静音门_源头工厂
product: 实心木门 (含双层阻尼静音条)
spec: 标准尺寸单开门
factory_price: 1800 # 单位: 元/樘
shipping: 厂家包安装
lead_time: 定制期(20天)
stage: 04_泥瓦完工后进场复尺
rating: 5
```

```yaml
id: M_PAINT_001
category: 辅材机电
brand: 立邦_总代直供
product: 全屋大白漆 (一底两面)
spec: 18L 大桶装
factory_price: 35 # 单位: 元/平米 (折算)
shipping: 满额包邮
lead_time: 现货(2天送达)
stage: 03_木工完工后进场
rating: 5
```

## 02. 辅材与机电

```yaml
id: M_PIPE_001
category: 隐蔽工程
brand: 伟星管业
product: 基础水电极客包 (强制水压测试+绝缘终端)
spec: 200平米大平层标准包
factory_price: 45000 # 单位: 元/整包
shipping: 满5000包邮
lead_time: 现货(1-2天送达)
stage: 01_水电交底阶段进场
rating: 5
```

## 03. 软装与家具

```yaml
id: M_SOFA_001
category: 软装家具
brand: 某意式极简复刻工坊
product: 大象耳朵科技布沙发
spec: 3.2米直排
factory_price: 5800 # 单位: 元/套
shipping: 顺丰包邮入户
lead_time: 定制期(15天)
stage: 05_保洁完成后进场
rating: 5
```
