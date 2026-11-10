#!/usr/bin/env python3
"""Generate exact, original SVG teaching diagrams; no trained CARAFE output is claimed."""
from html import escape
from pathlib import Path
import math
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/figures/upsampling'
X = [[10., 20.], [30., 40.]]

def sample_bilinear(i, j):
    y = min(max((i + .5) / 2 - .5, 0), 1)
    x = min(max((j + .5) / 2 - .5, 0), 1)
    return (1-y)*((1-x)*10+x*20)+y*((1-x)*30+x*40)

NEAREST = [[X[i//2][j//2] for j in range(4)] for i in range(4)]
BILINEAR = [[sample_bilinear(i,j) for j in range(4)] for i in range(4)]
PATCH = [[0,0,0], [10,20,0], [30,40,0]]
WEIGHTS = [[.01,.01,.01], [.10,.70,.01], [.05,.10,.01]]
CARAFE_TOY = sum(PATCH[i][j]*WEIGHTS[i][j] for i in range(3) for j in range(3))

def text(x,y,value,cls='',anchor='start',fill=None):
    return f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}"'+(f' fill="{fill}"' if fill else '')+f'>{escape(str(value))}</text>'

def arrow(x1,y1,x2,y2):
    return f'<path d="M{x1} {y1} L{x2} {y2}" class="arrow"/>'

def rect(x,y,w,h,fill='#f5f8fc',stroke='#ccd8e4',radius=8):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'

def number(v):
    return f'{v:g}' if isinstance(v,(int,float)) else str(v)

def matrix(values,x,y,cell=72,selected=None,weights=False):
    result=''
    for i,row in enumerate(values):
        for j,v in enumerate(row):
            if weights:
                alpha=float(v)
                fill=f'rgb({int(246-150*alpha)}, {int(248-125*alpha)}, {int(251-80*alpha)})'
            elif isinstance(v,(float,int)):
                alpha=max(0,min(float(v)/40,1))
                fill=f'rgb({int(245-100*alpha)}, {int(248-65*alpha)}, {int(251-25*alpha)})'
            else:fill='#f7f8fa'
            result+=rect(x+j*cell,y+i*cell,cell,cell,fill,'#d0dbe6',0)
            result+=text(x+(j+.5)*cell,y+(i+.5)*cell+10,number(v),'num','middle')
            if selected==(i,j):
                result+=f'<rect x="{x+j*cell+2}" y="{y+i*cell+2}" width="{cell-4}" height="{cell-4}" fill="none" stroke="#b46d16" stroke-width="4"/>'
    return result

def save(name,title,description,height,body):
    OUT.mkdir(parents=True,exist_ok=True)
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="{height}" viewBox="0 0 960 {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>
<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="#5b7892"/></marker></defs>
<style>text{{font-family:Arial,'Microsoft YaHei','PingFang SC',sans-serif;fill:#24394d;font-size:24px}}.title{{font-size:30px;font-weight:700}}.label{{font-size:25px;font-weight:600}}.small{{font-size:19px;fill:#52697d}}.num{{font-size:31px;font-variant-numeric:tabular-nums}}.arrow{{stroke:#5b7892;stroke-width:3;fill:none;marker-end:url(#arrow)}}</style>
<rect width="960" height="{height}" fill="white"/>
{text(35,47,title,'title')}{body}
</svg>'''
    (OUT/name).write_text(svg)

def main():
    assert BILINEAR == [[10,12.5,17.5,20],[15,17.5,22.5,25],[25,27.5,32.5,35],[30,32.5,37.5,40]]
    assert math.isclose(sum(map(sum,WEIGHTS)),1)
    assert math.isclose(CARAFE_TOY,20.5)

    body=text(80,106,'同一个输入：单个特征通道','label')+matrix(X,105,155,100)
    body+=arrow(340,250,442,250)+text(389,222,'×2','label','middle')
    body+=text(510,106,'每个值复制到 2 × 2 区域','label')+matrix(NEAREST,520,135,75,selected=(1,2))
    body+=text(80,480,'输出第 2 行、第 3 列（索引 [1,2]）= 20','label')
    body+=text(80,523,'最近邻：取一个值，不混合周围像素。此例中权重等价于 1、0、0、0。','small')
    save('01-nearest.svg','最近邻：直接复制附近的值','2×2 特征图最近邻放大至4×4，目标输出位置的值为20。',560,body)

    body=text(50,106,'先把输出位置映射回输入坐标','label')
    rows=[['输出列索引 j','0','1','2','3'],['映射坐标 x','−0.25','0.25','0.75','1.25'],['边界处理后','0','0.25','0.75','1']]
    widths=[230,150,150,150,150]
    for i,row in enumerate(rows):
        left=45
        for j,v in enumerate(row):
            body+=rect(left,130+i*55,widths[j],55,'#edf3fa' if j==3 else '#f7f9fb',radius=0)
            body+=text(left+widths[j]/2,165+i*55,v,'small' if j==0 else '', 'middle')
            left+=widths[j]
    body+=text(50,337,'输入 2 × 2','label')+matrix(X,70,370,72)
    body+=arrow(270,440,435,440)+text(350,408,'同样规则算 16 个位置','small','middle')
    body+=matrix(BILINEAR,510,315,68,selected=(1,2))
    body+=text(50,640,'本例 align_corners=False：x = (j + 0.5) / 2 − 0.5；纵向同理。','small')
    body+=text(50,677,'超出输入中心范围时采用边界值；右图高亮格的值是 22.5。','small')
    save('02-bilinear-grid.svg','双线性：每一个新位置都有对应坐标','半像素坐标约定下的2×2到4×4双线性数值结果。',710,body)

    body=text(45,102,'目标：输出索引 [1,2] → 输入坐标 (x,y) = (0.75,0.25)','label')
    body+=text(45,155,'四个输入值','label')+matrix(X,55,185,88)
    body+=arrow(258,270,326,270)+text(365,155,'按距离得到的权重','label')
    body+=matrix([[.1875,.5625],[.0625,.1875]],350,185,105,weights=True)
    body+=arrow(590,270,650,270)+rect(690,219,200,106,'#fff6e6','#dab773')
    body+=text(790,283,'22.5','title','middle')
    body+=text(45,426,'先横向：10×0.25 + 20×0.75 = 17.5','label')
    body+=text(45,467,'             30×0.25 + 40×0.75 = 37.5','label')
    body+=text(45,516,'再纵向：17.5×0.75 + 37.5×0.25 = 22.5','label')
    body+=text(45,569,'横向更靠近右侧 → 右侧权重 0.75；纵向更靠近上方 → 上方权重 0.75。','small')
    save('03-bilinear-one-pixel.svg','22.5 到底怎么算出来？','详细演算输出第2行第3列：按x与y的距离比例进行两次线性插值。',610,body)

    body=text(45,103,'预测支路：读取局部内容 → 生成每个新位置的权重','label')
    boxes=[(45,145,210,'1×1 卷积','压缩特征通道'),(355,145,230,'内容编码卷积','每个原位置输出 4×9 分数'),(690,145,225,'重排 + softmax','每个新位置的 9 项单独归一化')]
    for x,y,w,a,b in boxes:
        body+=rect(x,y,w,116)+text(x+w/2,y+43,a,'label','middle')
        # Split the long encoder and normalizer labels over two lines.
        lines={'每个原位置输出 4×9 分数':['每个原位置','输出 4×9 分数'],'每个新位置的 9 项单独归一化':['每个新位置的 9 项','单独归一化']}.get(b,[b])
        for j,line in enumerate(lines):body+=text(x+w/2,y+76+25*j,line,'small','middle')
    body+=arrow(267,201,341,201)+arrow(597,201,675,201)
    body+=text(45,319,'重组支路：原始邻域特征 × 预测权重 → 求和','label')
    body+=rect(45,355,285,92)+text(187,411,'取对应原位置的 3×3 邻域','small','middle')
    body+=arrow(345,400,420,400)+rect(437,355,225,92)+text(550,411,'9 项逐一相乘后求和','small','middle')
    body+=arrow(675,400,735,400)+rect(752,355,165,92,'#eef6f1','#a4c4b3')+text(835,411,'一个新值','label','middle')
    body+=text(45,496,'本例放大 2 倍：每个原位置对应 4 个子位置；每个子位置需要一套 3×3 核。','small')
    body+=text(45,533,'原始特征参与重组；压缩特征仅用于预测权重。示意配置，不是训练结果。','small')
    save('04-carafe-flow.svg','CARAFE：网络先预测权重，再重组特征','内容编码器读取局部特征，输出四套九项分数；各套独立softmax后重组原特征。',570,body)

    body=text(40,103,'仍计算输出索引 [1,2]；对应低分辨率位置 [0,1]（值 20）','label')
    body+=text(45,154,'3×3 输入邻域','label')+matrix(PATCH,50,185,74,selected=(1,1))
    body+=text(45,442,'灰色 0 是越界零填充','small')
    body+=arrow(292,298,342,298)+text(393,154,'假设预测出的示意权重','label')
    body+=matrix(WEIGHTS,385,185,74,weights=True)
    body+=text(400,442,'9 个权重之和 = 1','small')
    body+=arrow(630,298,685,298)+rect(717,252,195,96,'#fff6e6','#dab773')
    body+=text(815,310,'20.5','title','middle')
    body+=text(45,496,'10×0.10 + 20×0.70 + 30×0.05 + 40×0.10 = 20.5','label')
    body+=text(45,539,'这套核仅用于手算：没有训练好的预测网络，就不能确定真实 CARAFE 输出。','small')
    save('05-carafe-one-pixel.svg','同一个新位置，换成内容相关的权重','采用同一2×2输入的零填充3×3邻域与示意权重，计算20.5；不是模型预测。',580,body)

    body=text(45,103,'转置卷积：每个输入展开一个小核，重叠处相加','label')
    body+=text(45,144,'一维简例：输入 [10,20]；stride=2；示意核 [1,2,1]；padding=0','small')
    body+=text(45,214,'10 的贡献','small')+matrix([[10,20,10,0,0]],245,170,76)
    body+=text(45,296,'20 的贡献','small')+matrix([[0,0,20,40,20]],245,252,76)
    body+=text(45,378,'相加得到','label')+matrix([[10,20,30,40,20]],245,334,76,selected=(0,2))
    body+=text(45,454,'Pixel Shuffle：把通道里的数搬到空间位置','label')
    body+=text(45,497,'4 个通道：[10] [20] [30] [40]','label')
    body+=arrow(555,490,645,490)+matrix(X,710,447,63)
    body+=text(45,558,'重排本身没有可学习参数；前置卷积负责生成这些通道值。','small')
    body+=text(45,601,'以上是机制简例：转置卷积的核为示意值，不能作为真实网络输出。','small')
    save('06-other-operators.svg','另外两条路线：展开相加，或通道重排','用一维卷积和四通道单像素的小例子说明转置卷积与Pixel Shuffle。',640,body)

    (OUT/'example-values.json').write_text(json.dumps({'input':X,'nearest':NEAREST,'bilinear_align_corners_false':BILINEAR,'selected_output_index':[1,2],'bilinear_selected':22.5,'carafe_zero_padded_patch':PATCH,'carafe_illustrative_weights':WEIGHTS,'carafe_illustrative_value':CARAFE_TOY,'carafe_is_trained_output':False},ensure_ascii=False,indent=2)+'\n')
    print('Generated 6 original SVGs. Bilinear target=22.5; illustrative CARAFE target=20.5.')

if __name__ == '__main__':
    main()
