<!-- JavaScript สำหรับควบคุมการแสดง/ซ่อนกล่องไดอะล็อก -->
const deleteBtns = document.querySelectorAll('.delete-btn'); // ปุ่มลบสินค้าทั้งหมด
const deleteDialog = document.getElementById('deleteDialog');
const cancelDeleteBtn = document.getElementById('cancelDeleteBtn');


// ตรวจสอบการมีอยู่ของปุ่มลบ และเพิ่ม event listener
deleteBtns.forEach(button => {
    button.addEventListener('click', () => {
        // แสดงกล่องแจ้งเตือน
        deleteDialog.classList.remove('hidden');
    });
});

// ถ้าผู้ใช้กดยกเลิก, ซ่อนกล่องแจ้งเตือน
if (cancelDeleteBtn) {
    cancelDeleteBtn.addEventListener('click', () => {
        deleteDialog.classList.add('hidden');
    });
}
