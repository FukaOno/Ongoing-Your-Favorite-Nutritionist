A project that generates personalized one day meal plan based on users' previous meals to ensure a balanced diet

# -- Backend -- 
# Database-> MySQL-> Nutritions DB
1. Nutrition Amount for each ingredients/foods✅
- CNF Data/USDA https://www.canada.ca/en/health-canada/services/food-nutrition/healthy-eating/nutrient-data/canadian-nutrient-file-compilation-canadian-food-composition-data-database-structure.html 
- Parse with Python in MySQL✅
 - Food Name.csv (FoodID, FoodSourceID)✅🚨
 - Food Group.csv✅
 - Measure Name.csv(MeasureID)✅🚨
 - Conversion Factor.csv (MeasureID & Food ID)✅🚨
 - Food Source.csv✅
 - Nutrient Name.csv(NutrientsID)✅
 - Nutrient Amount.csv✅🚨
 - Nutrient Sources.csv✅


- Turn into an endpoint (able to query through HTTP) -> store in DB(connect MySQL)✅
-> to be able to retrive data✅

- generate meal plan templates 
   spoonacular API-> https://www.postman.com/spoonacular-api/spoonacular-api/request/m1148g0/search-recipes 


2. The target calorie calculator
https://www.myfitnesspal.com/ja/food/diary to get the target amount by this website
-> (Eventually do with web scrape or API)
-> save that data in MySQL database for tracking user data

3. calculate gaps with target nutritions (calories, fat, carbs, protein)




# -- Frontend -- React
Allow users to input their meals from the previous day and dietary preferences.

- Use Figma for design

- Create a form to collect:
  Previous meals (e.g., breakfast, lunch, dinner).-> https://www.myfitnesspal.com/ja/food/diary 
  Dietary preferences (e.g., vegetarian, vegan, gluten-free).
  Allergies or restrictions (e.g., nuts, lactose).

- Use JavaScript to validate inputs and dynamically adjust the form (e.g., show additional options if "vegan" is selected).


Present the generated meal plan to the user in an appealing format

- Use JavaScript to dynamically update the UI with meal suggestions.
- Include features to allow users to:
  - Swap meals.
  - See nutritional details for each meal.
  
Example display: const mealPlan = [
    { meal: "Breakfast", suggestion: "Oatmeal with fruits", nutrients: "Vitamin A: 20%, Iron: 15%" },
    { meal: "Lunch", suggestion: "Grilled chicken salad", nutrients: "Protein: 40g, Calcium: 30%" },
];
mealPlan.forEach(item => {
    const div = document.createElement("div");
    div.innerHTML = `<h3>${item.meal}</h3><p>${item.suggestion}</p><p>${item.nutrients}</p>`;
    document.body.appendChild(div);
});

- Add About the Data section to see the Resource (FNDDS resource)