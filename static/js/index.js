const uploadForm = document.getElementById("uploadForm");
const progressBar = document.querySelector(".progress-bar");
const fileInput = document.getElementById("fileInput");
const fileContent = document.querySelector(".file-name");

fileInput.addEventListener("change", function () {
    if (fileInput.files.length > 0) {
        fileContent.textContent = fileInput.files[0].name;
    }
});

uploadForm.addEventListener("submit", function (e) {
    e.preventDefault();

    const formData = new FormData(uploadForm);
    const xhr = new XMLHttpRequest();

    xhr.open("POST", "/upload", true);

    // 🔥 Track upload progress
    xhr.upload.addEventListener("progress", function (e) {
        if (e.lengthComputable) {
            const percent = (e.loaded / e.total) * 100;

            progressBar.style.width = percent + "%";
            progressBar.setAttribute("aria-valuenow", percent);
            progressBar.textContent = Math.round(percent) + "%";
        }
    });

    // ✅ When upload finishes
    xhr.onload = function () {
        if (xhr.status === 200) {
            progressBar.classList.add("bg-success");
            alert("Upload successful!");
        } else {
            progressBar.classList.add("bg-danger");
            alert("Upload failed.");
        }
    };

    xhr.send(formData);
});