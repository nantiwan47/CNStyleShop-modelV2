// ฟังก์ชันเพิ่มตัวเลือกสีใหม่
function addColorOption() {
    const colorOptionsContainer = document.getElementById('color-options-container');
    const newColorOption = document.createElement('div');
    newColorOption.classList.add('color-option');

    newColorOption.innerHTML = `
        <label>สี:</label>
        <input type="text" name="colors[]" required>
        
        <label>อัปโหลดภาพสำหรับสีนี้:</label>
        <input type="file" name="color_images[]" required>
        
        <h4>ตัวเลือกไซส์และราคา</h4>
        <div class="size-price-container">
            <label>Size:</label>
            <input type="text" name="sizes[]" required>
            
            <label>ราคา:</label>
            <input type="text" name="prices[]" required>
        </div>
        <button type="button" onclick="addSizeOption(this)">เพิ่มไซส์</button><br><br>
    `;

    colorOptionsContainer.appendChild(newColorOption);
}

// ฟังก์ชันเพิ่มตัวเลือกไซส์ใหม่
function addSizeOption(button) {
    const sizePriceContainer = button.closest('.color-option').querySelector('.size-price-container');
    const newSizeOption = document.createElement('div');

    newSizeOption.innerHTML = `
        <label>Size:</label>
        <input type="text" name="sizes[]" required>
        
        <label>ราคา:</label>
        <input type="text" name="prices[]" required>
    `;

    sizePriceContainer.appendChild(newSizeOption);
}

// ฟังก์ชันเตรียมข้อมูลและส่งฟอร์ม
function prepareData(event) {
    event.preventDefault();  // ป้องกันไม่ให้ฟอร์มส่งข้อมูลเอง

    const formData = new FormData();
    const colorOptions = document.querySelectorAll('.color-option');

    colorOptions.forEach((colorOption) => {
        const color = colorOption.querySelector('input[name="colors[]"]').value;
        const image = colorOption.querySelector('input[name="color_images[]"]').files[0];
        const sizes = Array.from(colorOption.querySelectorAll('input[name="sizes[]"]')).map(input => input.value);
        const prices = Array.from(colorOption.querySelectorAll('input[name="prices[]"]')).map(input => input.value);

        formData.append('colors[]', color);
        formData.append('color_images[]', image);  // ส่งไฟล์จริง

        sizes.forEach((size, i) => {
            formData.append('sizes[]', size);
            formData.append('prices[]', prices[i]);
        });
    });

    // // ส่งข้อมูลไปยังเซิร์ฟเวอร์
    // fetch('/path-to-your-endpoint', {
    //     method: 'POST',
    //     body: formData  // ส่งข้อมูลทั้งหมดเป็น FormData
    // }).then(response => response.json())
    //   .then(data => console.log(data))  // รับข้อมูลจากเซิร์ฟเวอร์
    //   .catch(error => console.error('Error:', error));
}
