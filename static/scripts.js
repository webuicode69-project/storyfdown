const btn = document.getElementById("downloadBtn");
const input = document.getElementById("urlInput");
const result = document.getElementById("result");
const video = document.getElementById("videoPreview");
const link = document.getElementById("downloadLink");
const errorMsg = document.getElementById("errorMsg");
const loader = document.getElementById("loader");
const pasteBtn = document.getElementById("pasteBtn");
const themeToggle = document.getElementById("themeToggle");

/* 🌗 DARK / LIGHT MODE */
themeToggle.addEventListener("click", () => {
    document.body.classList.toggle("light");

    if (document.body.classList.contains("light")) {
        themeToggle.innerText = "☀️";
        localStorage.setItem("theme", "light");
    } else {
        themeToggle.innerText = "🌙";
        localStorage.setItem("theme", "dark");
    }
});

/* load saved theme */
if (localStorage.getItem("theme") === "light") {
    document.body.classList.add("light");
    themeToggle.innerText = "☀️";
}

/* 📋 AUTO PASTE */
pasteBtn.addEventListener("click", async () => {
    try {
        const text = await navigator.clipboard.readText();
        input.value = text;
    } catch {
        alert("Gagal akses clipboard");
    }
});

/* AUTO DETECT PASTE (HP modern) */
window.addEventListener("load", async () => {
    try {
        const text = await navigator.clipboard.readText();
        if (text.includes("facebook.com")) {
            input.value = text;
        }
    } catch {}
});

/* DOWNLOAD */
btn.addEventListener("click", async () => {

    const url = input.value.trim();

    if (!url) {
        errorMsg.innerText = "Masukkan URL terlebih dahulu";
        errorMsg.classList.remove("hidden");
        return;
    }

    errorMsg.classList.add("hidden");
    result.classList.add("hidden");

    loader.classList.remove("hidden");
    btn.disabled = true;

    try {
        const res = await fetch("/api/download", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ url })
        });

        const data = await res.json();

        if (data.status === "success") {
            const videoUrl = data.hd || data.sd;

            video.src = videoUrl;
            link.href = videoUrl;

            result.classList.remove("hidden");
        } else {
            errorMsg.innerText = data.message;
            errorMsg.classList.remove("hidden");
        }

    } catch {
        errorMsg.innerText = "Server error";
        errorMsg.classList.remove("hidden");
    }

    loader.classList.add("hidden");
    btn.disabled = false;
});