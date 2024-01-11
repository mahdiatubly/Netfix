document.addEventListener("DOMContentLoaded", function () {
    // Get the current URL
    var currentURL = window.location.href;

    // Get the box element by its ID
    var customerBox = document.getElementById("customer-section");
    var companyrBox = document.getElementById("company-section");   

    // Check conditions and change background color
    if (currentURL.includes("customer/signup")) {
        customerBox.style.backgroundColor = "#a8a6a6";
        var customerAnchor = document.getElementById('customer-url');
        customerAnchor.href = "#";
        var companyAnchor = document.getElementById('company-url');
        companyAnchor.href = "/users/company/signup";
    } else if (currentURL.includes("company/signup")) {
        companyrBox.style.backgroundColor = "#a8a6a6";
        var customerAnchor = document.getElementById('customer-url');
        customerAnchor.href = "/users/customer/signup";
        var companyAnchor = document.getElementById('company-url');
        companyAnchor.href = "#";
    }
});