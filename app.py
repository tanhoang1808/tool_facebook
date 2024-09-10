from flask import Flask, request, render_template, jsonify
import os
from invite import main  # Import hàm main từ file invite.py

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Tạo thư mục nếu chưa tồn tại
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Định nghĩa trang chính
@app.route('/')
def index():
    return render_template('index.html')

# Xử lý form và upload cookie và uid_group
@app.route('/submit', methods=['POST'])
def submit():
    try:
        cookies = request.form['cookies']
        uid_group = request.form['uid_group']
        uids = request.form.getlist('uids[]')  # Nhận danh sách UID

        # Lưu danh sách UID vào file 
        with open('uid.txt', 'w') as f:
            for uid in uids:
                f.write(uid + "\n")

        # Gọi hàm chính để xử lý và lấy kết quả
        results = []
        for uid in uids:
            result = main(cookies, uid_group)
            if result == 200:
                results.append({'uid': uid, 'status': 'success'})
            elif result == 201:
                results.append({'uid': uid, 'status': 'failure', 'reason': "Cant Add User to Group"})
            elif result == 202:
                results.append({'uid': uid, 'status': 'done'})
        
        return jsonify({'uids': results}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
