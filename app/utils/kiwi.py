from typing import List

from openai import OpenAIError

from app import kiwi_client
from app.models import MessageRole


def kiwi_format_history(history: List):
    return [{
            "role": item.message_role,
            "content": item.content
        } for item in history
    ]
    
def kiwi_create_prompt(message: str, course, comments):
    return [{
        "role": "system",
        "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"
    }, {
        "role": "system",
        "content": f"你现在作为评论分析员，根据评论分析指定课程，不同评论使用\'<sep>\'间隔，评论含有评分，分值1-5，分值越高评价越好，最高5分; 如果没有评论，请你只结合课程介绍进行分析。课程为{course.coursename}，课程介绍为{course.description}，评论有{'<sep>'.join(f'{c.content} 评分{c.star}' for c in comments)}。"
    }]
    
def kiwi(message: str, context: List):
    try:
        completion = kiwi_client.chat.completions.create(
            model="moonshot-v1-8k",
            messages=context + [{
                "role": MessageRole.USER.value, 
                "content": message
            }],
            temperature=0.3
        )
    except OpenAIError as e:
        print(f"error: ", e)
        return {}, False
    else:
        return {
            "role": MessageRole.ASSISTANT.value, 
            "content": completion.choices[0].message.content
        }, True