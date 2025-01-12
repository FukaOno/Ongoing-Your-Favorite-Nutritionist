const mealPlan = [
    { meal: "Breakfast", suggestion: "Oatmeal with fruits" },
    { meal: "Lunch", suggestion: "Grilled chicken salad" },
    { meal: "Dinner", suggestion: "Quinoa and roasted vegetables" }
];
mealPlan.forEach(item => {
    const div = document.createElement("div");
    div.innerHTML = `<h3>${item.meal}</h3><p>${item.suggestion}</p>`;
    document.body.appendChild(div);
});
