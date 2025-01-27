// script.js

// Event listener untuk tombol logout (jika ingin menambahkan animasi atau konfirmasi sebelum logout)
document.querySelector('.logout-button').addEventListener('click', function(e) {
    const confirmLogout = confirm("Are you sure you want to logout?");
    if (!confirmLogout) {
        e.preventDefault(); // Menghentikan logout jika tidak dikonfirmasi
    }
});
