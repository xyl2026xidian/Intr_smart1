# ============================================================
# 文件名: module1_intro.py
# 说明: 智能制造工程导论 - 模块一 智能学习交互页面
# 功能: 3D知识图谱 + 交互探索 + 趣味匹配 + 成就系统
# 运行: streamlit run module1_intro.py
# ============================================================

import streamlit as st
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import random
import time
from datetime import datetime

st.set_page_config(
    page_title="模块一 · 智能制造导论",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ======================= 自定义CSS =======================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif; }
    .main-header { font-size: 2.8rem; font-weight: 800; background: linear-gradient(135deg, #1a3a5c, #4a90d9); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; margin-bottom: 5px; }
    .sub-header { font-size: 1.1rem; color: #6c757d; text-align: center; margin-bottom: 20px; }
    .glow-card { background: linear-gradient(135deg, #ffffff, #f8f9fa); border-radius: 16px; padding: 20px; box-shadow: 0 8px 30px rgba(0,0,0,0.08); border: 1px solid rgba(255,255,255,0.5); transition: transform 0.3s ease; }
    .glow-card:hover { transform: translateY(-4px); box-shadow: 0 12px 40px rgba(26,58,92,0.15); }
    .badge { display: inline-block; background: linear-gradient(135deg, #ffd700, #ffb300); color: #1a3a5c; padding: 4px 14px; border-radius: 20px; font-size: 0.75rem; font-weight: 700; }
    .progress-text { font-size: 0.9rem; color: #495057; }
    .knowledge-node { cursor: pointer; transition: all 0.3s; }
    .knowledge-node:hover { transform: scale(1.15); }
    .stButton>button { background: linear-gradient(135deg, #1a3a5c, #2c5f8a); color: white; border: none; border-radius: 10px; padding: 10px 24px; font-weight: 600; transition: all 0.3s; }
    .stButton>button:hover { transform: scale(1.03); box-shadow: 0 6px 20px rgba(26,58,92,0.3); }
    .match-card { background: white; border-radius: 12px; padding: 15px; border: 2px solid #e9ecef; text-align: center; cursor: pointer; transition: all 0.3s; }
    .match-card:hover { border-color: #2c5f8a; transform: scale(1.02); }
    .match-card.selected { border-color: #2c5f8a; background: #e8f4fd; }
    .match-card.matched { border-color: #28a745; background: #e6f7e6; }
    .achievement { background: linear-gradient(135deg, #fff8e1, #fff3cd); border-radius: 12px; padding: 12px; border: 1px solid #ffd700; text-align: center; }
    .float-animation { animation: float 3s ease-in-out infinite; }
    @keyframes float { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-8px); } }
</style>
""", unsafe_allow_html=True)

# ======================= 会话状态初始化 =======================
if 'module1_progress' not in st.session_state:
    st.session_state.module1_progress = 0
if 'achievements' not in st.session_state:
    st.session_state.achievements = []
if 'matched_pairs' not in st.session_state:
    st.session_state.matched_pairs = []
if 'selected_card' not in st.session_state:
    st.session_state.selected_card = None
if 'interest_score' not in st.session_state:
    st.session_state.interest_score = 0
if 'explored_nodes' not in st.session_state:
    st.session_state.explored_nodes = set()

# ======================= 知识节点数据 =======================
KNOWLEDGE_NODES = [
    {"id": "HCPS", "label": "HCPS", "desc": "人-信息-物理系统，智能制造的核心框架", "color": "#FF6B6B", "x": 0, "y": 2, "z": 0},
    {"id": "数字化", "label": "数字化", "desc": "物理→数字，让制造可计算", "color": "#4ECDC4", "x": -2, "y": 1, "z": 0.5},
    {"id": "网络化", "label": "网络化", "desc": "设备→互联，让制造可连接", "color": "#45B7D1", "x": 2, "y": 1, "z": -0.3},
    {"id": "智能化", "label": "智能化", "desc": "数据→智能，让制造可思考", "color": "#96CEB4", "x": -1.5, "y": 0, "z": -1},
    {"id": "机器人", "label": "🤖 智能装备", "desc": "工业机器人、数控机床、AGV", "color": "#FFEAA7", "x": 1.5, "y": 0, "z": 1.2},
    {"id": "数字孪生", "label": "🔄 数字孪生", "desc": "物理-虚拟双向映射，实时交互", "color": "#DDA0DD", "x": 0, "y": -1, "z": 0.8},
    {"id": "工业互联网", "label": "🌐 工业互联网", "desc": "设备联网、数据中台、协同制造", "color": "#87CEEB", "x": -1.2, "y": -1.2, "z": -0.5},
    {"id": "人工智能", "label": "🧠 人工智能", "desc": "大模型、智能体、机器视觉", "color": "#F0A0A0", "x": 1.2, "y": -0.8, "z": -1.2},
]

# ======================= 匹配游戏数据 =======================
MATCH_PAIRS = [
    ("HCPS", "人-信息-物理系统"),
    ("数字孪生", "物理-虚拟双向映射"),
    ("工业互联网", "设备联网协同制造"),
    ("数字化", "物理→数字可计算"),
    ("智能化", "数据驱动智能决策"),
]

# ======================= 主界面 =======================
st.markdown('<div class="main-header">🚀 智能制造 · 探索之旅</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">模块一：从机械制造到智能制造的范式跃迁</div>', unsafe_allow_html=True)

# ===== 顶部状态栏 =====
col_status1, col_status2, col_status3, col_status4 = st.columns(4)
with col_status1:
    progress_pct = min(100, int(st.session_state.module1_progress / len(KNOWLEDGE_NODES) * 100))
    st.markdown(f"📊 **探索进度**  \n{progress_pct}%")
    st.progress(progress_pct/100)
with col_status2:
    st.markdown(f"🏆 **成就**  \n{len(st.session_state.achievements)} 个")
with col_status3:
    st.markdown(f"⭐ **兴趣分**  \n{st.session_state.interest_score}")
with col_status4:
    st.markdown(f"💡 **已探索**  \n{len(st.session_state.explored_nodes)}/{len(KNOWLEDGE_NODES)}")

st.markdown("---")

# ===== 主布局：左中右 =====
col_left, col_center, col_right = st.columns([1.5, 3, 1.5])

# ===== 左侧：学习引导 =====
with col_left:
    st.markdown('<div class="glow-card">', unsafe_allow_html=True)
    st.markdown("### 🎯 今日学习目标")
    st.markdown("""
    1. 理解智能制造的核心定义  
    2. 掌握 HCPS 三层架构  
    3. 了解三大赋能技术  
    4. 认识智能装备与系统  
    """)
    st.markdown("---")
    st.markdown("### 📖 核心概念速览")
    concepts = ["制造强国战略", "新质生产力", "数字化转型", "智能化升级"]
    for c in concepts:
        st.markdown(f"• {c}")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown('<div class="glow-card" style="margin-top:12px;">', unsafe_allow_html=True)
    st.markdown("### 🎮 学习模式")
    mode = st.radio("", ["🔬 探索模式", "📚 阅读模式", "🧩 挑战模式"], index=0)
    st.markdown("</div>", unsafe_allow_html=True)

# ===== 中间：3D 知识星球 =====
with col_center:
    st.markdown('<div class="glow-card">', unsafe_allow_html=True)
    st.markdown("### 🌍 智能制造知识星球")
    st.markdown("*点击节点展开知识点 · 拖拽旋转*")
    
    # 构建3D散点图
    fig = go.Figure()
    
    x_vals = [n["x"] for n in KNOWLEDGE_NODES]
    y_vals = [n["y"] for n in KNOWLEDGE_NODES]
    z_vals = [n["z"] for n in KNOWLEDGE_NODES]
    labels = [n["label"] for n in KNOWLEDGE_NODES]
    colors = [n["color"] for n in KNOWLEDGE_NODES]
    
    # 节点连线（生成知识网络）
    for i in range(len(KNOWLEDGE_NODES)):
        for j in range(i+1, len(KNOWLEDGE_NODES)):
            if np.random.random() > 0.5:  # 随机连线，视觉美观
                fig.add_trace(go.Scatter3d(
                    x=[x_vals[i], x_vals[j]],
                    y=[y_vals[i], y_vals[j]],
                    z=[z_vals[i], z_vals[j]],
                    mode='lines',
                    line=dict(color='rgba(200,200,200,0.3)', width=1),
                    showlegend=False,
                    hoverinfo='none'
                ))
    
    # 主节点
    fig.add_trace(go.Scatter3d(
        x=x_vals,
        y=y_vals,
        z=z_vals,
        mode='markers+text',
        marker=dict(
            size=25,
            color=colors,
            symbol='circle',
            line=dict(color='white', width=2),
            opacity=0.9
        ),
        text=labels,
        textposition='top center',
        textfont=dict(size=10, color='#1a3a5c', family='Inter'),
        hoverinfo='text',
        hovertext=[n["desc"] for n in KNOWLEDGE_NODES],
        customdata=[n["id"] for n in KNOWLEDGE_NODES],
        name='知识节点'
    ))
    
    fig.update_layout(
        scene=dict(
            xaxis=dict(showbackground=False, showgrid=False, showticklabels=False, title=''),
            yaxis=dict(showbackground=False, showgrid=False, showticklabels=False, title=''),
            zaxis=dict(showbackground=False, showgrid=False, showticklabels=False, title=''),
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.2)),
            annotations=[]
        ),
        height=420,
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
        hovermode='closest',
        clickmode='event'
    )
    
    st.plotly_chart(fig, use_container_width=True, key='knowledge_graph')
    
    # 节点点击交互（通过按钮模拟）
    st.markdown("**📌 快速探索**")
    cols = st.columns(4)
    for i, node in enumerate(KNOWLEDGE_NODES[:4]):
        with cols[i]:
            if st.button(node["label"], key=f"node_{node['id']}", use_container_width=True):
                st.session_state.explored_nodes.add(node["id"])
                st.session_state.module1_progress = len(st.session_state.explored_nodes)
                st.session_state.interest_score += 5
                if len(st.session_state.explored_nodes) >= 3 and "探索者" not in st.session_state.achievements:
                    st.session_state.achievements.append("探索者")
                st.success(f"✨ {node['desc']}")
                time.sleep(0.5)
                st.rerun()
    
    st.caption("💡 点击上方按钮或3D节点探索知识点 | 每探索一个知识点 +5 兴趣分")
    st.markdown("</div>", unsafe_allow_html=True)

# ===== 右侧：成就与兴趣 =====
with col_right:
    st.markdown('<div class="glow-card">', unsafe_allow_html=True)
    st.markdown("### 🏅 成就徽章")
    if st.session_state.achievements:
        for a in st.session_state.achievements:
            st.markdown(f"""
            <div class="achievement">
                🎖️ <strong>{a}</strong> — 解锁成功！
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align:center;color:#adb5bd;padding:20px;">
            <div style="font-size:3rem;">🔒</div>
            <p>探索3个知识点解锁「探索者」</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📊 学习热情")
    heat = min(100, st.session_state.interest_score * 2)
    st.metric("🔥 学习热度", f"{min(100, heat)}%")
    st.caption("每探索一个知识点热度+10%")
    
    st.markdown("---")
    st.markdown("### ⏱️ 学习建议")
    if st.session_state.module1_progress < 3:
        st.info("💡 建议：点击上方3D节点探索基础知识")
    elif st.session_state.module1_progress < 5:
        st.success("👍 继续探索！你已经掌握了核心概念")
    else:
        st.success("🎉 太棒了！你已掌握模块一核心知识，可以进行匹配挑战！")
    st.markdown("</div>", unsafe_allow_html=True)

# ===== 底部：匹配挑战 =====
st.markdown("---")
st.markdown("### 🧩 知识匹配挑战")

col_game1, col_game2, col_game3 = st.columns([2, 1, 2])

with col_game2:
    st.markdown("将左侧术语与右侧定义匹配")
    if st.button("🔄 重新洗牌", use_container_width=True):
        st.session_state.matched_pairs = []
        st.session_state.selected_card = None
        st.rerun()
    if len(st.session_state.matched_pairs) == len(MATCH_PAIRS):
        st.success("🎉 全部匹配成功！")
        if "匹配大师" not in st.session_state.achievements:
            st.session_state.achievements.append("匹配大师")
            st.session_state.interest_score += 20

col_left_match, col_right_match = st.columns(2)

with col_left_match:
    st.markdown("**📌 术语**")
    terms = [p[0] for p in MATCH_PAIRS if p not in st.session_state.matched_pairs]
    for term in terms:
        is_selected = (st.session_state.selected_card == term)
        bg_color = "#e8f4fd" if is_selected else "white"
        st.markdown(f"""
        <div class="match-card {'selected' if is_selected else ''}" 
             onclick="console.log('{term}')" style="background:{bg_color};">
            {term}
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"选择 {term}", key=f"sel_{term}", use_container_width=True):
            if term not in [p[0] for p in st.session_state.matched_pairs]:
                st.session_state.selected_card = term
                st.rerun()

with col_right_match:
    st.markdown("**📖 定义**")
    for term, defin in MATCH_PAIRS:
        if [term, defin] not in st.session_state.matched_pairs:
            if st.button(f"配对: {defin}", key=f"match_{term}", use_container_width=True):
                if st.session_state.selected_card == term:
                    st.session_state.matched_pairs.append([term, defin])
                    st.session_state.interest_score += 10
                    st.session_state.selected_card = None
                    if len(st.session_state.matched_pairs) >= 3 and "匹配新星" not in st.session_state.achievements:
                        st.session_state.achievements.append("匹配新星")
                    st.rerun()
                else:
                    st.warning(f"请先选择对应的术语再配对！")

# 已匹配展示
if st.session_state.matched_pairs:
    st.markdown("**✅ 已匹配：**")
    matched_text = ", ".join([f"{p[0]} ↔ {p[1]}" for p in st.session_state.matched_pairs])
    st.markdown(f"<div style='background:#e6f7e6;padding:10px;border-radius:8px;'>{matched_text}</div>", unsafe_allow_html=True)

# ===== 底部：学习总结 =====
st.markdown("---")
with st.expander("📝 学习总结与思考", expanded=False):
    st.markdown("""
    ### 本节课你学到了什么？
    - **智能制造** = 数字化 + 网络化 + 智能化 与制造技术的深度融合
    - **HCPS** = 人-信息-物理系统，是智能制造的核心理论框架
    - **三大赋能技术**：让制造可计算、可连接、可思考
    - **智能装备**：工业机器人、数控机床、AGV 等
    - **数字孪生**：物理-虚拟双向映射，实时交互与优化
    """)
    st.markdown("### 💬 你的学习感悟")
    feedback = st.text_area("记录你的想法...", placeholder="今天学到了什么？有什么疑问？")
    if feedback:
        st.success("📝 已记录！继续加油！")