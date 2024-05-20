import matplotlib.pyplot as plt

# 准备数据
x = [1, 2, 3, 4, 5]  # x轴数据
y = [10, 15, 13, 18, 16]  # y轴数据

# 使用plt.plot()函数绘制折线图
plt.plot(x, y)

# 添加标题和标签（可选）
plt.title('折线图示例')
plt.xlabel('X轴标签')
plt.ylabel('Y轴标签')

# 显示图形
plt.show()
    # 步驟3：調整音訊的採樣率
    target_sampling_rate = 16000
    data, sampling_rate = librosa.load(io.BytesIO(audio_bytes), sr=target_sampling_rate)
    
    # 步驟4：進行傅立葉轉換
    fft_data = np.fft.fft(audio_bytes)
    
    # 步驟5：顯示頻譜
    frequencies = np.fft.fftfreq(len(fft_data),1 / target_sampling_rate) #1 / target_sampling_rate(需要分析的音檔長度，取樣間隔)
    
    plt.figure(figsize=(12, 4))
    plt.plot(frequencies, np.abs(fft_data))
    plt.title('Spectrum')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.show()