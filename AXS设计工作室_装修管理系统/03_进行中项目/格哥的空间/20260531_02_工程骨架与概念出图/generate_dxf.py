import ezdxf

def generate_base_cad():
    # Create a new DXF document
    doc = ezdxf.new("R2010")
    msp = doc.modelspace()
    
    # Draw LDK Area (Living, Dining, Kitchen)
    msp.add_lwpolyline([(0, 0), (6000, 0), (6000, 8000), (0, 8000)], close=True, dxfattribs={'color': 1})
    msp.add_text("AXS_LDK_Area", dxfattribs={'height': 200, 'color': 1}).set_placement((2000, 4000))
    
    # Draw Master Bedroom Area
    msp.add_lwpolyline([(6000, 0), (10000, 0), (10000, 5000), (6000, 5000)], close=True, dxfattribs={'color': 2})
    msp.add_text("AXS_Master_Bed", dxfattribs={'height': 200, 'color': 2}).set_placement((7000, 2500))
    
    # Draw "Spiritual Corner" in Master Bed
    msp.add_lwpolyline([(8500, 3500), (10000, 3500), (10000, 5000), (8500, 5000)], close=True, dxfattribs={'color': 3})
    msp.add_text("AXS_Spiritual_Corner", dxfattribs={'height': 150, 'color': 3}).set_placement((8600, 4200))
    
    # Add an AI prompt for the user inside the CAD
    prompt_text = "AI_Prompt: Please stretch this box to adjust the Spiritual Corner area, then press Ctrl+S to save."
    msp.add_text(prompt_text, dxfattribs={'height': 150, 'color': 4}).set_placement((0, 8500))

    # Save to file
    filename = "格哥_AI概念骨架.dxf"
    doc.saveas(filename)
    print(f"✅ 成功生成实体 CAD 图纸: {filename}")

if __name__ == "__main__":
    generate_base_cad()
