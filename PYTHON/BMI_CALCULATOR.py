def calculate_bmi(weight, height):
    BMI = weight/ (height ** 2)
    return BMI

if __name__ == "__main__":
    weight = float(input("Enter weight in kg: "))
    height = float(input("Enter height in meters: "))
    print("Your BMI is:", calculate_bmi(weight, height))

if calculate_bmi(weight, height) < 18.5:
    print ("Underweight")
elif 18.5 <= calculate_bmi(weight, height) < 25:
    print ("Normal Weight")
elif 25 <= calculate_bmi(weight, height) < 30:
    print ("Overweight")
else:
    print ("Obese")

   