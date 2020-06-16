XLA_BTL
1. Đặt vấn đề: Chuyển đổi Ảnh về Text (OCR) - Chuyển đổi Captcha
2. Xây dựng models: 
    2.1: Chuẩn bị dữ liệu (10k ảnh captcha http://tracuunnt.gdt.gov.vn/tcnnt/mstdn.jsp)
    2.2: Khử nhiễu (Opencv)
    2.3: Cắt ảnh ( THuật toán Từ trái --> Phải )
    2.4: Dán nhãn 
        C1: Thủ công, kiểm tra băngf mắt -> dãn nhán kí tự
        C2: Dán nhãn băng pre-train model ( pytesseract - chạy nhanh, kết quả cho ra đúng tầm 60% )
    2.5: Build model: Sử dụng deep learning Convolutional Neural Network. Sử dụng FrameWork Keras
    2.6: Training model
    2.7: Predict 
3. Predict Captcha