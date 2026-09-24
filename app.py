from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# ========== 基础数据定义 ==========

# 性别映射
gender_map = {
    "女": "1girl",
    "男": "1boy"
}

# 年龄范围
age_range = list(range(20, 41))

# 人脸特征映射
face_map = {
    "东亚": "East Asian facial features, delicate features",
    "欧美": "European facial features, sharp facial structure, deep-set eyes",
    "非洲": "African facial features, rich skin tone, defined bone structure"
}

scene_list = [
    "sunlit rooftop, city background",
    "quiet forest trail, soft diffused light",
    "modern minimalist cafe, window side",
    "seaside beach at golden hour",
    "old bookstore, warm ambient light",
    "urban street at dusk, neon glow",
    "flower garden, spring cherry blossoms",
    "empty art gallery, clean white wall",
    "mountain overlook, cloud sea",
    "cozy bedroom, morning sunlight",
    "subway platform, soft cool tone",
    "lawn park, afternoon shade",
    "vintage street market",
    "glass greenhouse",
    "lakeside pier, sunset",
    "marble hall, simple interior",
    "rainy sidewalk, reflection",
    "rooftop night view, city lights",
    "bamboo grove, dappled light",
    "library reading corner"
]

pose_list = [
    "standing, gentle smile, hands naturally hanging",
    "sitting on bench, head slightly tilted",
    "leaning against wall, one hand in pocket",
    "walking forward, slight turn of head",
    "half squat, looking up",
    "resting elbow on table, chin on hand",
    "standing side profile, gaze far away",
    "sitting cross-legged",
    "holding hair with one hand",
    "turning back, looking over shoulder",
    "standing, arms crossed lightly",
    "sitting on stone step, knees together",
    "reaching hand toward flower",
    "leaning on railing",
    "slight bow, soft expression",
    "standing, one leg slightly forward",
    "sitting sideways",
    "raising hand to block sunlight",
    "resting hands behind back",
    "walking sideways"
]

outfit_list = [
    "white loose shirt + denim skirt",
    "cream knit sweater + long skirt",
    "simple linen dress",
    "casual blazer + wide pants",
    "vintage floral midi dress",
    "white tank top + high waist jeans",
    "trench coat, simple inner wear",
    "pleated skirt + college style shirt",
    "silk slip dress",
    "hoodie + jogger pants",
    "linen shirt + long trousers",
    "knit vest + white shirt",
    "denim jacket + short skirt",
    "chiffon long dress",
    "cropped cardigan + camisole",
    "canvas overalls",
    "tailored short suit",
    "velvet midi skirt + plain top",
    "striped shirt + long skirt",
    "lightweight windbreaker"
]

negative_prompt = "bad anatomy, deformed, extra limbs, missing fingers, ugly, blurry, lowres, disfigured, mutated, watermark, text, signature, oversaturated, bad proportions, cross-eye"

# 冲突规则
conflict_rules = {
    "rainy sidewalk, reflection": ["silk slip dress"],
    "seaside beach at golden hour": ["trench coat, simple inner wear", "cream knit sweater + long skirt"],
    "bamboo grove, dappled light": ["raising hand to block sunlight"],
    "subway platform, soft cool tone": ["velvet midi skirt + plain top"]
}

# ========== 路由 ==========

@app.route("/")
def index():
    return render_template(
        "index.html",
        ages=age_range,
        genders=list(gender_map.keys()),
        faces=list(face_map.keys()),
        scenes=scene_list,
        poses=pose_list,
        outfits=outfit_list
    )


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()

    age = data.get("age", "20")
    gender = data.get("gender", "女")
    face = data.get("face", "东亚")
    scene = data.get("scene", scene_list[0])
    pose = data.get("pose", pose_list[0])
    outfit = data.get("outfit", outfit_list[0])

    # 冲突检测
    warning = ""
    if scene in conflict_rules:
        banned = conflict_rules[scene]
        if outfit in banned or pose in banned:
            warning = f"⚠️ 冲突提醒：场景「{scene}」与所选穿搭/姿势不匹配，建议调整。"

    # 构建正向提示词
    gender_tag = gender_map.get(gender, "1girl")
    face_tag = face_map.get(face, face_map["东亚"])
    base_char = f"{gender_tag}, {age}yo, {face_tag}, realistic skin texture, ARRI Alexa65, Kodak Portra400, 8K, HDR, 50mm f1.8, cinematic lighting"
    positive = f"{base_char}, {scene}, {pose}, {outfit}"

    return jsonify({
        "positive": positive,
        "negative": negative_prompt,
        "warning": warning
    })


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)