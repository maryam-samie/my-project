import streamlit as st
import random
import time
import pandas as pd
import os
import math
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error
import joblib
st.set_page_config(page_title="سلام خیلی خوش اومدین")
tab1, tab2, tab3, tab4, tab5 = st.tabs(['game','report','dashboard','prediction', 'guideline'])

with tab1:
    choice = st.radio('Choose a game', ['game1', 'game2', 'game3'])
    
    if choice == 'game1':
        st.title("✊✋✌️ بازی سنگ، کاغذ، قیچی")
        
        CHOICES = ["سنگ", "کاغذ", "قیچی"]
        MAX_ROUNDS = 5
        RECORDS_FILE = "rps_records.csv"
        
        # گرفتن اسم بازیکن
        if "player_name" not in st.session_state:
            st.session_state.player_name = ""

        if not st.session_state.player_name:
            username_input = st.text_input("👤 نام خود را وارد کن:", "")
            if username_input:
                st.session_state.player_name = username_input
                st.rerun()
            else:
                st.stop()
        
        # مقداردهی اولیه
        if "round" not in st.session_state:
            st.session_state.round = 1
            st.session_state.player_wins = 0
            st.session_state.computer_wins = 0
            st.session_state.results = []
            st.session_state.finished = False
        
        st.markdown(f"### مرحله {st.session_state.round} از {MAX_ROUNDS}")
        
        # انتخاب بازیکن
        player_choice = st.radio("انتخاب کن:", CHOICES, horizontal=True)
        
        if st.button("✅ بازی کن"):
            computer_choice = random.choice(CHOICES)
        
            # تعیین برنده
            if player_choice == computer_choice:
                result = "مساوی 🤝"
            elif (player_choice == "سنگ" and computer_choice == "قیچی") or \
                 (player_choice == "کاغذ" and computer_choice == "سنگ") or \
                 (player_choice == "قیچی" and computer_choice == "کاغذ"):
                result = f"🏆 {st.session_state.player_name} برد!"
                st.session_state.player_wins += 1
            else:
                result = "💻 کامپیوتر برد!"
                st.session_state.computer_wins += 1
            
        
            # ذخیره نتیجه
            st.session_state.results.append({
                "round": st.session_state.round,
                "player": player_choice,
                "computer": computer_choice,
                "result": result
            })
        
            st.success(f"👤 {st.session_state.player_name}: {player_choice} | 💻 کامپیوتر: {computer_choice}")
            st.info(result)
            time.sleep(5)
        
            # مرحله بعد
            if st.session_state.round < MAX_ROUNDS:
                st.session_state.round += 1
                st.rerun()
            else:
                st.session_state.finished = True
        
        # پایان بازی
        if st.session_state.finished:
            st.markdown("---")
            st.header("🏁 پایان بازی")
        
            st.write("📋 نتایج مراحل:")
            for r in st.session_state.results:
                st.write(f"مرحله {r['round']}: 👤 {r['player']} vs 💻 {r['computer']} → {r['result']}")
        
            st.markdown(f"### 👤 {st.session_state.player_name} برد: {st.session_state.player_wins} مرحله")
            st.markdown(f"### 💻 کامپیوتر برد: {st.session_state.computer_wins} مرحله")
        
            # برنده نهایی
            if st.session_state.player_wins > st.session_state.computer_wins:
                st.success(f"🏆 تبریک! {st.session_state.player_name} برنده کل بازی شد!")
            elif st.session_state.player_wins < st.session_state.computer_wins:
                st.error("💻 کامپیوتر برنده کل بازی شد!")
            else:
                st.warning("🤝 بازی مساوی شد!")
        
            # ذخیره رکورد در فایل CSV
            new_record = {
                "نام": st.session_state.player_name,
                "برد بازیکن": st.session_state.player_wins,
                "برد کامپیوتر": st.session_state.computer_wins,
                "تعداد مراحل": MAX_ROUNDS
            }
        
            df_new = pd.DataFrame([new_record])
        
            if os.path.exists(RECORDS_FILE):
                df_all = pd.read_csv(RECORDS_FILE)
        
                # بروزرسانی رکورد در صورت بهتر بودن
                if st.session_state.player_name in df_all["نام"].values:
                    prev_wins = df_all.loc[df_all["نام"] == st.session_state.player_name, "برد بازیکن"].values[0]
                    if st.session_state.player_wins > prev_wins:
                        df_all.loc[df_all["نام"] == st.session_state.player_name] = new_record
                        st.success("🏆 رکورد قبلی‌ات بروزرسانی شد!")
                    else:
                        st.info("ℹ️ امتیازت کمتر از رکورد قبلیه. رکورد قبلی حفظ شد.")
                else:
                    df_all = pd.concat([df_all, df_new], ignore_index=True)
            else:
                df_all = df_new
        
            df_all.to_csv(RECORDS_FILE, index=False)
        
            # نمایش جدول رکوردها
            st.subheader("📋 جدول رکوردها")
            df_sorted = df_all.sort_values(by="برد بازیکن", ascending=False).reset_index(drop=True)
            st.dataframe(df_sorted)
        
            if st.button("🔁 شروع دوباره"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()


    elif choice == 'game2':
        st.title("🧠 بازی حافظه مرحله‌ای")
        
        # حداکثر مرحله
        MAX_LEVEL = 5
        
        emoji_pool = ["🍎", "🚗", "🐱", "🍕", "🏀", "🎲", "🎯", "🦊", "🎧", "📚", "🌈", "🎹"]
        
        # وضعیت بازی
        if 'level' not in st.session_state:
            st.session_state.level = 1
        if 'flipped' not in st.session_state:
            st.session_state.flipped = []
        if 'matched' not in st.session_state:
            st.session_state.matched = []
        if 'turns' not in st.session_state:
            st.session_state.turns = 0
        if 'last_choice' not in st.session_state:
            st.session_state.last_choice = None
        if 'start_time' not in st.session_state:
            st.session_state.start_time = time.time()
        if 'end_time' not in st.session_state:
            st.session_state.end_time = None
        if 'cards' not in st.session_state:
            st.session_state.cards = []
        
        def generate_cards(level):
            num_pairs = level + 2
            emojis = random.sample(emoji_pool, num_pairs) * 2
            random.shuffle(emojis)
            return emojis
        
        def reset_game(level=1):
            st.session_state.level = level
            st.session_state.cards = generate_cards(level)
            num_cards = len(st.session_state.cards)
            st.session_state.flipped = [False] * num_cards
            st.session_state.matched = [False] * num_cards
            st.session_state.turns = 0
            st.session_state.last_choice = None
            st.session_state.start_time = time.time()
            st.session_state.end_time = None
        
        if st.button("🔄 شروع دوباره از مرحله ۱"):
            reset_game(1)
        
        if len(st.session_state.cards) == 0:
            reset_game(st.session_state.level)
        
        # چیدمان کارت‌ها
        num_cards = len(st.session_state.cards)
        cols_per_row = 4
        rows = math.ceil(num_cards / cols_per_row)
        
        for row in range(rows):
            cols = st.columns(cols_per_row)
            for col in range(cols_per_row):
                idx = row * cols_per_row + col
                if idx >= num_cards:
                    break
                with cols[col]:
                    if st.session_state.flipped[idx] or st.session_state.matched[idx]:
                        st.button(st.session_state.cards[idx], key=f"card_{idx}", disabled=True)
                    else:
                        if st.button("❓", key=f"card_{idx}"):
                            st.session_state.flipped[idx] = True
                            if st.session_state.last_choice is None:
                                st.session_state.last_choice = idx
                            else:
                                j = st.session_state.last_choice
                                st.session_state.turns += 1
                                if st.session_state.cards[idx] == st.session_state.cards[j]:
                                    st.session_state.matched[idx] = True
                                    st.session_state.matched[j] = True
                                else:
                                    time.sleep(0.5)
                                    st.session_state.flipped[idx] = False
                                    st.session_state.flipped[j] = False
                                st.session_state.last_choice = None
                            st.rerun()
        
        # اطلاعات بازی
        st.markdown(f"### 🌟 مرحله: {st.session_state.level} از {MAX_LEVEL}")
        st.markdown(f"✨ تعداد تلاش‌ها: {st.session_state.turns}")
        
        # پایان مرحله
        if all(st.session_state.matched):
            if st.session_state.end_time is None:
                st.session_state.end_time = time.time()
            total_time = st.session_state.end_time - st.session_state.start_time
            st.success("🎉 آفرین! این مرحله رو تموم کردی!")
            st.markdown(f"⏱️ زمان: **{total_time:.2f} ثانیه**")
        
            if st.session_state.level < MAX_LEVEL:
                if st.button("🚀 رفتن به مرحله بعد"):
                    reset_game(st.session_state.level + 1)
            else:
                st.balloons()
                st.markdown("🏁 بازی تموم شد! همه مراحل رو گذروندی! آفرین 👏")
                if st.button("🔁 شروع دوباره"):
                    reset_game(1)

    elif choice == 'game3': 
        # عنوان و توضیحات بازی ۳
        st.title("⌨️ بازی چالش تایپ – مرحله‌ای + جدول رکورد")
        st.caption("🏆 رکورد بزن و دقت تایپت رو بسنج!")

        sample_texts = [
            "زندگی یعنی حرکت. هر چه بیشتر تلاش کنی، بیشتر موفق خواهی شد.",
            "موفقیت چیزی نیست جز تکرارِ تمرین، پشتکار، و ایمان به خود.",
            "در تاریکی، حتی یک شمع کوچک هم می‌تواند راه را روشن کند.",
            "فکر مثبت، شروع تغییرات بزرگ است.",
            "هیچ چیز غیرممکن نیست اگر باورش کنی.",
            "باور به خود اولین قدم موفقیت است.",
            "امروزت را طوری بساز که فردا به خودت افتخار کنی.",
            "تنها راه شکست نخوردن، تلاش مداوم است.",
            "هیچ‌وقت برای شروع دیر نیست.",
            "با برنامه‌ریزی می‌توان به هر چیزی رسید."
        ]
        
        MAX_ROUNDS = 5
        RECORDS_FILE = "typing_records.csv"
        
        # ورود نام کاربر فقط بار اول
        if "username" not in st.session_state:
           st.session_state.username = ""

        if not st.session_state.username:
            username_input = st.text_input("👤 نام خود را وارد کن:", "")
            if username_input:
                st.session_state.username = username_input
                st.rerun()
            else:
                st.stop()
        
        # مقداردهی اولیه session_state
        if "round" not in st.session_state:
            st.session_state.round = 1
            st.session_state.start_time = None
            st.session_state.score_list = []
            st.session_state.accuracies = []
            st.session_state.times = []
            st.session_state.current_text = random.choice(sample_texts)
            st.session_state.finished = False
        
        st.markdown(f"### مرحله {st.session_state.round} از {MAX_ROUNDS}")
        st.code(st.session_state.current_text, language="")
        
        # ناحیه تایپ
        typed_text = st.text_area("📝 متن بالا را تایپ کن:", height=150)
        
        # شروع تایمر
        if typed_text and st.session_state.start_time is None:
            st.session_state.start_time = time.time()
        
        # دکمه پایان مرحله
        if st.button("✅ پایان مرحله"):
            if not typed_text.strip():
                st.warning("لطفاً متن را تایپ کن.")
            else:
                end_time = time.time()
                duration = end_time - st.session_state.start_time
                correct_chars = sum(1 for i, c in enumerate(typed_text) if i < len(st.session_state.current_text) and c == st.session_state.current_text[i])
                accuracy = round((correct_chars / len(st.session_state.current_text)) * 100, 2)
                score = round(accuracy * (1 / (duration + 1)) * 10, 2)
        
                st.session_state.score_list.append(score)
                st.session_state.accuracies.append(accuracy)
                st.session_state.times.append(duration)
        
                st.success("🎯 مرحله به پایان رسید!")
                st.markdown(f"⏱ زمان: **{round(duration, 2)} ثانیه**")
                st.markdown(f"🎯 دقت: **{accuracy}%**")
                st.markdown(f"🏆 امتیاز این مرحله: **{score}**")
                time.sleep(5)
        
                if st.session_state.round < MAX_ROUNDS:
                    st.session_state.round += 1
                    st.session_state.current_text = random.choice(sample_texts)
                    st.session_state.start_time = None
                    st.rerun()
                else:
                    st.session_state.finished = True
        
        # پایان بازی
        if st.session_state.finished:
            st.markdown("---")
            st.header("🏁 پایان بازی")
        
            total_score = round(sum(st.session_state.score_list), 2)
            avg_accuracy = round(sum(st.session_state.accuracies) / MAX_ROUNDS, 2)
            avg_time = round(sum(st.session_state.times) / MAX_ROUNDS, 2)
        
            st.markdown(f"👤 **نام:** {st.session_state.username}")
            st.markdown(f"🧠 **میانگین دقت:** {avg_accuracy}%")
            st.markdown(f"⏱ **میانگین زمان:** {avg_time} ثانیه")
            st.markdown(f"🏆 **امتیاز نهایی:** {total_score} ⭐️")
        
            # ذخیره رکورد در فایل CSV
            new_record = {
    "نام": st.session_state.username,
    "امتیاز نهایی": total_score,
    "میانگین دقت (%)": avg_accuracy,
    "میانگین زمان (ثانیه)": avg_time,
    "تعداد مراحل": MAX_ROUNDS
}

            df_new = pd.DataFrame([new_record])
        
            if os.path.exists(RECORDS_FILE):
                df_all = pd.read_csv(RECORDS_FILE)
                if "نام" not in df_all.columns:  # اطمینان از ستون نام
                    df_all["نام"] = ""
                if st.session_state.username in df_all["نام"].values:
                    prev_score = df_all.loc[df_all["نام"] == st.session_state.username, "امتیاز نهایی"].values[0]
                    if total_score > prev_score:
                        df_all.loc[df_all["نام"] == st.session_state.username] = new_record
                        st.success("🏆 رکورد قبلی‌ات بروزرسانی شد!")
                    else:
                        st.info("ℹ️ امتیازت کمتر از رکورد قبلیه. رکورد قبلی حفظ شد.")
                else:
                    df_all = pd.concat([df_all, df_new], ignore_index=True)
            else:
                df_all = df_new
            
            df_all.to_csv(RECORDS_FILE, index=False, encoding="utf-8-sig")
            
            
            # جدول رکوردها
            st.subheader("📋 جدول رکوردها")
            df_sorted = df_all.sort_values(by="امتیاز نهایی", ascending=False).reset_index(drop=True)
            st.dataframe(df_sorted)
        
            # دکمه شروع دوباره
            if st.button("🔄 شروع دوباره"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
with tab2:
    st.write('wwww')
with tab3:
    st.write('zzz')
with tab4:
    df = pd.read_csv(r"F:\data analyist\final project\machine learning\StudentPerformanceFactors.csv")
    df.head()
    # ⚙️ بخش 3: آموزش مدل یادگیری ماشین
    
    # جداسازی ویژگی‌ها و متغیر هدف
    X = df.drop("Exam_Score", axis=1)
    y = df["Exam_Score"]
    
    # ستون‌های عددی و دسته‌ای
    categorical_cols = X.select_dtypes(include=["object"]).columns.tolist()
    numerical_cols = X.select_dtypes(exclude=["object"]).columns.tolist()
    
    # پیش‌پردازش: One-Hot Encoding برای ستون‌های دسته‌ای
    preprocessor = ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols)
    ], remainder="passthrough")
    
    # ساخت pipeline
    model = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("regressor", RandomForestRegressor(random_state=42))
    ])
    
    # تقسیم داده‌ها
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # آموزش مدل
    model.fit(X_train, y_train)
    
    # ارزیابی مدل
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    print(f"میانگین خطای مطلق (MAE): {mae:.2f}")
    
    # ذخیره مدل
    joblib.dump(model, "student_performance_model.pkl")
    # 🖥️ بخش 4: طراحی فرم Streamlit برای پیش‌بینی نمره
    
    st.set_page_config(page_title="Student Exam Score Predictor", page_icon="🎓")
    st.title("🎓 پیش‌بینی نمره امتحانی دانش‌آموز")
    
    model = joblib.load("student_performance_model.pkl")
    
    # فرم ورودی
    hours = st.slider("⏱ ساعات مطالعه در هفته", 0, 40, 10)
    attendance = st.slider("📈 درصد حضور در کلاس", 0, 100, 85)
    parental = st.selectbox("👨‍👩‍👧‍👦 میزان درگیری والدین", ["Low", "Medium", "High"])
    resources = st.selectbox("📚 دسترسی به منابع", ["Low", "Medium", "High"])
    extra = st.selectbox("🏀 فعالیت‌های فوق برنامه", ["Yes", "No"])
    sleep = st.slider("🛌 ساعات خواب شبانه", 0, 12, 7)
    previous = st.slider("📊 نمرات قبلی", 0, 100, 70)
    motivation = st.selectbox("🔥 سطح انگیزه", ["Low", "Medium", "High"])
    internet = st.selectbox("🌐 دسترسی به اینترنت", ["Yes", "No"])
    tutoring = st.slider("📘 تعداد جلسات کمک‌درسی", 0, 10, 1)
    income = st.selectbox("💵 درآمد خانواده", ["Low", "Medium", "High"])
    teacher = st.selectbox("🧑‍🏫 کیفیت معلم", ["Low", "Medium", "High"])
    school = st.selectbox("🏫 نوع مدرسه", ["Public", "Private"])
    peer = st.selectbox("👫 تأثیر هم‌سالان", ["Positive", "Neutral", "Negative"])
    activity = st.slider("🏃 فعالیت بدنی هفتگی", 0, 10, 3)
    disability = st.selectbox("🧠 ناتوانی یادگیری", ["Yes", "No"])
    parent_edu = st.selectbox("🎓 سطح تحصیلات والدین", ["High School", "College", "Postgraduate"])
    distance = st.selectbox("📍 فاصله خانه تا مدرسه", ["Near", "Moderate", "Far"])
    gender = st.selectbox("👤 جنسیت", ["Male", "Female"])
    
    if st.button("📊 پیش‌بینی نمره"):
        input_df = pd.DataFrame([{
            "Hours_Studied": hours,
            "Attendance": attendance,
            "Parental_Involvement": parental,
            "Access_to_Resources": resources,
            "Extracurricular_Activities": extra,
            "Sleep_Hours": sleep,
            "Previous_Scores": previous,
            "Motivation_Level": motivation,
            "Internet_Access": internet,
            "Tutoring_Sessions": tutoring,
            "Family_Income": income,
            "Teacher_Quality": teacher,
            "School_Type": school,
            "Peer_Influence": peer,
            "Physical_Activity": activity,
            "Learning_Disabilities": disability,
            "Parental_Education_Level": parent_edu,
            "Distance_from_Home": distance,
            "Gender": gender
        }])
    
        predicted_score = model.predict(input_df)[0]
        st.success(f"🎯 نمره پیش‌بینی شده: {predicted_score:.2f}")

with tab5:
    st.write('qqqq')