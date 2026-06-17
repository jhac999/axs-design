import ezdxf

def create_extreme_dxf(filename):
    # 创建一个新的 DXF 文档
    doc = ezdxf.new(dxfversion="R2010")
    msp = doc.modelspace()
    
    # 建立特殊图层
    doc.layers.add("AXS_动线留白禁区", color=2) # 黄色
    doc.layers.add("AXS_绝对收纳红线", color=1) # 红色
    doc.layers.add("AXS_精神角落屏蔽区", color=3) # 绿色
    doc.layers.add("AXS_资金熔断禁飞区", color=1) # 红色
    doc.layers.add("AXS_声学强制隔离带", color=4) # 青色
    
    # 1. 餐厅中枢 (强制通顶餐边柜)
    msp.add_lwpolyline([(4000, 2000), (6400, 2000), (6400, 2400), (4000, 2400)], close=True, dxfattribs={'layer': 'AXS_绝对收纳红线'})
    msp.add_text("AXS_强制通顶餐边柜 (深度40cm/无拉手/一抹到底)", dxfattribs={'layer': 'AXS_绝对收纳红线', 'height': 150}).set_placement((4100, 2500))
    
    # 2. 资金熔断禁飞区 (绝对禁止电视背景墙与酒柜)
    msp.add_lwpolyline([(3000, 7500), (9000, 7500), (9000, 8000), (3000, 8000)], close=True, dxfattribs={'layer': 'AXS_资金熔断禁飞区'})
    # 交叉警戒线
    msp.add_line((3000, 7500), (9000, 8000), dxfattribs={'layer': 'AXS_资金熔断禁飞区'})
    msp.add_line((3000, 8000), (9000, 7500), dxfattribs={'layer': 'AXS_资金熔断禁飞区'})
    msp.add_text("AXS_禁飞区: 严禁电视背景墙/酒柜 (全白留白保命)", dxfattribs={'layer': 'AXS_资金熔断禁飞区', 'height': 150}).set_placement((3100, 7300))
    
    # 3. 声学隔离带 (下水管包双层隔音棉)
    msp.add_circle((11000, 7000), radius=200, dxfattribs={'layer': 'AXS_声学强制隔离带'})
    msp.add_text("AXS_声学隔离: 下水管强制双层阻尼隔音", dxfattribs={'layer': 'AXS_声学强制隔离带', 'height': 150}).set_placement((8500, 6900))
    
    # 4. 精神角落屏蔽区 (解决“减压”)
    msp.add_lwpolyline([(8000, 3000), (10000, 3000), (10000, 4400), (8000, 4400)], close=True, dxfattribs={'layer': 'AXS_精神角落屏蔽区'})
    msp.add_text("AXS_男主人情绪充电桩 (强制留白 + 2700K 氛围光)", dxfattribs={'layer': 'AXS_精神角落屏蔽区', 'height': 120}).set_placement((8100, 3600))
    
    # 外框 (房屋外墙示意)
    msp.add_lwpolyline([(0, 0), (12000, 0), (12000, 8000), (0, 8000)], close=True)

    doc.saveas(filename)
    print(f"成功生成硬核参数化 CAD 图纸: {filename}")

if __name__ == "__main__":
    create_extreme_dxf("格哥_审计官终极自检版.dxf")
