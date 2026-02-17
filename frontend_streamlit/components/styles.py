"""
Styles CSS modernes
"""
import streamlit as st

def load_css():
    """Charge les styles CSS"""
    st.markdown("""
    <style>
        /* Header principal */
        .main-header {
            background: linear-gradient(135deg, #06D6A0 0%, #118AB2 100%);
            padding: 40px;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        /* Carte annonce */
        .annonce-card {
            background: white;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            border-left: 5px solid #06D6A0;
            box-shadow: 0 5px 15px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
        }
        
        .annonce-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        }
        
        /* Badge promu */
        .promu-badge {
            background: #FFD166;
            color: #333;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
            display: inline-block;
        }
        
        /* Cartes stats */
        .stat-card {
            background: white;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 3px 10px rgba(0,0,0,0.05);
            border-top: 4px solid #06D6A0;
        }
        
        /* Boutons */
        .btn-action {
            background: #06D6A0;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s;
            margin: 2px;
        }
        
        .btn-action:hover {
            background: #05C592;
            transform: scale(1.05);
        }
        
        .btn-fav {
            background: #FFD166;
            color: #333;
        }
        
        .btn-fav:hover {
            background: #FFC745;
        }
        
        /* Messages */
        .message-sent {
            background: #06D6A0;
            color: white;
            padding: 12px 16px;
            border-radius: 18px 18px 4px 18px;
            margin: 8px 0;
            max-width: 70%;
            margin-left: auto;
        }
        
        .message-received {
            background: #F0F0F0;
            color: #333;
            padding: 12px 16px;
            border-radius: 18px 18px 18px 4px;
            margin: 8px 0;
            max-width: 70%;
        }
        
        /* Navigation */
        .nav-button {
            width: 100%;
            text-align: left;
            padding: 12px 20px;
            margin: 5px 0;
            border-radius: 8px;
            border: none;
            background: transparent;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .nav-button:hover {
            background: rgba(6, 214, 160, 0.1);
        }
        
        /* Cartes dans grid */
        .annonce-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        /* Tags */
        .tag {
            display: inline-block;
            background: #E9F7F2;
            color: #06D6A0;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 12px;
            margin: 2px;
        }
        
        /* Footer annonce */
        .annonce-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #eee;
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .annonce-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
    """, unsafe_allow_html=True)