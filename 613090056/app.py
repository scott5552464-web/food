# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 13:25:07 2026

@author: Administrator
"""

from flask import Flask, render_template, request

app = Flask(__name__)

# 食物健康分數資料庫
food_scores = {
    "雞胸肉": 20,
    "青菜": 20,
    "高麗菜": 20,
    "花椰菜": 20,
    "水果": 15,
    "蘋果": 15,
    "香蕉": 15,
    "橘子": 15,
    "牛奶": 10,
    "豆漿": 10,
    "蛋": 10,
    "白飯": 5,
    "糙米飯": 10,
    "地瓜": 10,
    "魚": 15,
    "鮭魚": 20,

    "炸雞": -25,
    "漢堡": -20,
    "薯條": -20,
    "可樂": -20,
    "珍珠奶茶": -25,
    "披薩": -20,
    "泡麵": -25,
    "炸豬排": -20,
    "香腸": -15,
    "蛋糕": -15,
    "餅乾": -10
}


def calculate_score(text):
    score = 50

    healthy = []
    unhealthy = []

    for food, value in food_scores.items():
        if food in text:
            score += value
            if value > 0:
                healthy.append(food)
            else:
                unhealthy.append(food)

    if score > 100:
        score = 100

    if score < 0:
        score = 0

    return score, healthy, unhealthy


@app.route("/", methods=["GET", "POST"])
def index():

    result = None
    advice = ""

    if request.method == "POST":

        breakfast = request.form.get("breakfast", "")
        lunch = request.form.get("lunch", "")
        dinner = request.form.get("dinner", "")

        all_food = breakfast + lunch + dinner

        score, healthy, unhealthy = calculate_score(all_food)

        if score >= 90:
            level = "★★★★★ 非常健康"
        elif score >= 75:
            level = "★★★★☆ 很健康"
        elif score >= 60:
            level = "★★★☆☆ 普通"
        elif score >= 40:
            level = "★★☆☆☆ 需要改善"
        else:
            level = "★☆☆☆☆ 不健康"

        if score >= 80:
            advice = "飲食相當均衡，請繼續保持！"
        elif score >= 60:
            advice = "可以再增加蔬菜與水果。"
        else:
            advice = "建議少吃油炸及含糖飲料，多補充天然食物。"

        result = {
            "score": score,
            "level": level,
            "healthy": healthy,
            "unhealthy": unhealthy
        }

    return render_template(
        "index.html",
        result=result,
        advice=advice
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)