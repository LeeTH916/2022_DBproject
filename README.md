# 2022_DBproject

● 주요 제공 기능 
- 기능 1 : 가지고 있는 음식 재료 확인 가능
- 기능 2 : 가지고 있는 음식의 주재료에 대한 여러 가지 메뉴 확인 가능
- 기능 3 : 해당 메뉴에 필요한 재료 및 추가로 구매가 필요한 재료 확인 가능
- 기능 4 : 해당 메뉴의 조리과정 확인 가능
- 기능 5 : 유통기한이 임박한(7일 이하) 재료 확인 가능
- 기능 6 : 가지고 있는 음식 재료 데이터베이스에 재료 추가 및 삭제 가능

● 동작 시나리오
서비스의 형태를 앱이라고 가정할 때 앱을 실행하면 
1. 메뉴 이름 확인을 위한 MenuList를 레시피 기본정보 API를 통해 받아온다. 
2. 가지고 있는 음식 데이터베이스 MyIngredient로부터 분류가 주재료인 재료들의 이름을 받
아와 저장한다.
3. comboBox를 이용해 주재료들 중 하나를 선택하면 재료 이름을 통해 레시피 재료정보
API를 활용하여 Recipe_ID를 받아오고 이것을 MenuList와 매칭하여 메뉴의 이름까지 함께
 저장한 후 comboBox_2에 보여준다.
4. comboBox_2에서 메뉴를 선택하면 해당 메뉴의 RecipeID를 통해 레시피 재료정보 API를
 활용하여 해당 메뉴에 필요한 재료 목록을 받아와서 보여주고 저장한 후 MyIngredient로부
터 모든 재료들의 이름을 받아와 MyIngredient에 없는 재료를 확인하여 추가로 구매가 필요
한 재료들을 보여준다.
5. 메뉴가 선택된 상황에서 레시피 보기 버튼을 누를 경우 해당 메뉴의 RecipeID를 통해 레
시피 과정정보 API를 활용하여 해당 메뉴에 대한 조리과정을 보여준다.
6. 있는 재료 보기 버튼을 누를 경우 MyIngredient에 있는 모든 재료의 목록을 보여준다.
7. 유통기한 임박 재료 보기 버튼을 누를 경우 유통기한과 현재 날짜의 차이를 계산해 유통기
한이 7일 이하인 재료들을 보여준다.
8. 재료를 구매하거나 사용한 경우 MyIngredient에 추가하거나 삭제한다.
