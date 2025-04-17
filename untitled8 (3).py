# -*- coding: utf-8 -*-
"""Untitled8.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1oV_fTNmrTqtG5YhvjgQt2f-5DEWTaZIa
"""

import os

pip install -r requirements.txt

pip install streamlit

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import os

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import os

# Removed or renamed in newer Streamlit versions
# st.set_option('deprecation.showPyplotGlobalUse', False)
st.title("Fall Detection with LSTM")

# ... (rest of your code remains the same) ...




#st.set_option('deprecation.showPyplotGlobalUse', False)
st.title("Fall Detection with LSTM")

# Upload the Excel file
uploaded_file = st.file_uploader("/content/glasses1_part1_features_added.xlsx", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Simulate labels if missing
    if 'LABEL' not in df.columns:
        df['LABEL'] = 0
        df.loc[df['JERK_MAG'] > df['JERK_MAG'].quantile(0.95), 'LABEL'] = 1  # simulate falls

    # Feature distribution plots
    st.subheader("Feature Distributions by LABEL")
    features_to_plot = ['ACC_MAG', 'JERK_MAG', 'GYRO_MAG', 'PITCH', 'ROLL', 'SVM']
    for feature in features_to_plot:
        sns.histplot(df, x=feature, hue='LABEL', kde=True, element='step')
        st.pyplot()

    # Prepare data
    feature_cols = ['ACC_X', 'ACC_Y', 'ACC_Z', 'JERK_X', 'JERK_Y', 'JERK_Z',
                    'GYRO_X', 'GYRO_Y', 'GYRO_Z', 'PITCH', 'ROLL', 'SVM']

    X = df[feature_cols].values
    y = df['LABEL'].values

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    SEQ_LEN = 10
    def create_sequences(X, y, seq_len):
        X_seq, y_seq = [], []
        for i in range(len(X) - seq_len):
            X_seq.append(X[i:i+seq_len])
            y_seq.append(y[i+seq_len])
        return np.array(X_seq), np.array(y_seq)

    X_seq, y_seq = create_sequences(X_scaled, y, SEQ_LEN)

    X_train, X_test, y_train, y_test = train_test_split(X_seq, y_seq, test_size=0.2, random_state=42)

    # LSTM model
    model = Sequential()
    model.add(LSTM(64, input_shape=(SEQ_LEN, X.shape[1]), return_sequences=False))
    model.add(Dropout(0.3))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    st.subheader("Training Model...")
    history = model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2, verbose=0)

    loss, accuracy = model.evaluate(X_test, y_test)
    st.success(f"Test Accuracy: {accuracy:.2f}")

    st.subheader("Training History")
    fig, ax = plt.subplots(1, 2, figsize=(12, 4))
    ax[0].plot(history.history['loss'], label="Train Loss")
    ax[0].plot(history.history['val_loss'], label="Val Loss")
    ax[0].legend()
    ax[0].set_title("Loss")

    ax[1].plot(history.history['accuracy'], label="Train Acc")
    ax[1].plot(history.history['val_accuracy'], label="Val Acc")
    ax[1].legend()
    ax[1].set_title("Accuracy")

    st.pyplot(fig)

