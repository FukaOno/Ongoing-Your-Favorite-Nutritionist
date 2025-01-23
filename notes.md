A project that generates personalized one day meal plan based on users' previous meals to ensure a balanced diet

# Functionality and notes

# -- Backend -- 
Analyze user input to identify nutritional gaps.

# Database-> MySQL-> storing meal data and nutritional info
+The previous day's calories, fat, carbs, protein calculator-> now use the outside url
https://www.myfitnesspal.com/ja/food/diary to calculate 
-> also get the target amount by this website
-> save that data in MySQL database for tracking data

- Create a SQL schema for storing two tables -> one day nutritional data (per category) and target amount(per day)✅
- Focus on carbs, protein, fat (macronutrients)
- for one day nutritional data-> the id link to three category✅
- Add sample data to test queries✅
- calculate gaps with SQL(Make total_calories column...-> total - target= gap)✅


# Nutrition DataBase

- Automate the process of getting accurate nutritional data for specific food items
   USDA FoodData Central API-> https://fdc.nal.usda.gov/api-guide
   -> Food Details endpoint, which returns details on a particular food
   -> ❌couldnt get the foodID

- Web scrape 10,0000+ items  Python and bs4(Beautiful Soup 4), to populate Database (not manually enter) with accurate and relevant food nutrient information
   -> ❌no good web only for nutrition data(usually need to add the ingredients)

- Excel Data from Food and Nutrient Database for Dietary Studies (FNDDS)
https://www.ars.usda.gov/northeast-area/beltsville-md-bhnrc/beltsville-human-nutrition-research-center/food-surveys-research-group/docs/fndds-download-databases/ 
4 excel sheets-> 11,848 Foods  
  -> convert into csv(2021-2023)✅, (2019-2020)✅,(2017-2018)✅, (2015-2016)✅ -> Data Cleaning✅⭐️ -> Turn into an endpoint (able to query through HTTP) by parse with python✅-> store in DB(connect MySQL)

- generate meal plan templates 
   spoonacular API-> https://www.postman.com/spoonacular-api/spoonacular-api/request/m1148g0/search-recipes 

# -- Frontend -- HTML, CSS, JavaScript
Allow users to input their meals from the previous day and dietary preferences.

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