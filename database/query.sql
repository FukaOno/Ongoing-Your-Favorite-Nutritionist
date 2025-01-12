SELECT target_nutrients.user_id, meals.category, meals.calories, meals.protein, meals.carbs, meals.fat FROM meals
LEFT JOIN target_nutrients ON meals.user_id = target_nutrients.user_id
WHERE target_nutrients.user_id = 1;



SELECT t.user_id, 
t.target_calories - IFNULL(m.total_calories, 0) AS calorie_gap, 
t.target_protein - IFNULL(m.total_protein, 0) AS protein_gap, 
t.target_carbs - IFNULL(m.total_carbs, 0) AS carbs_gap,
t.target_fat - IFNULL(m.total_fat, 0) AS fat_gap
FROM target_nutrients AS t
LEFT JOIN (SELECT user_id, 
SUM(calories) AS total_calories, 
SUM(protein) AS total_protein, 
SUM(carbs) AS total_carbs, 
SUM(fat) AS total_fat
FROM meals
GROUP BY user_id) AS m ON t.id = m.user_id
WHERE t.user_id = 1;







