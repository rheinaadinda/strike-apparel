function showToast(title, message, type = 'normal', duration = 3000) {
    const toast = document.getElementById('toast-component');
    const toastTitle = document.getElementById('toast-title');
    const toastMessage = document.getElementById('toast-message');
    const toastIcon = document.getElementById('toast-icon');

    if (!toast) return;

    // reset semua style
    toast.className = 'fixed bottom-8 right-8 z-50 w-80 p-4 px-6 rounded-xl backdrop-blur-md bg-white/80 border border-white/30 shadow-lg flex items-start gap-4 opacity-0 pointer-events-none transform translate-y-12 transition-all duration-300 ease-in-out';
    toastIcon.textContent = '';

    // type styling & icon (ubah ke tema biru)
    if (type === 'success') {
        toast.classList.add('border-[#57A0D3]', 'text-[#3579aa]');
        toastIcon.textContent = '✔️';
    } else if (type === 'error') {
        toast.classList.add('border-red-400', 'text-red-700');
        toastIcon.textContent = '❌';
    } else if (type === 'info') {
        toast.classList.add('border-[#57A0D3]', 'text-[#57A0D3]');
        toastIcon.textContent = 'ℹ️';
    } else {
        toast.classList.add('border-gray-300', 'text-gray-800');
        toastIcon.textContent = '💬';
    }

    toastTitle.textContent = title;
    toastMessage.textContent = message;

    // tampilkan dengan animasi dari bawah
    toast.classList.remove('opacity-0', 'translate-y-12');
    toast.classList.add('opacity-100', 'translate-y-0', 'pointer-events-auto');

    // sembunyikan setelah duration
    setTimeout(() => {
        toast.classList.remove('opacity-100', 'translate-y-0', 'pointer-events-auto');
        toast.classList.add('opacity-0', 'translate-y-12');
    }, duration);
}
