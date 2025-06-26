from selene import browser, have, be, by
import os

from selene.api import command


def test_submit_student_registration_form():
    # 1. Открыть страницу с формой
    browser.open("/")  # Замените на ваш URL

    # 2. Заполнить обязательные поля
    browser.element("#firstName").type("Иван")
    browser.element("#lastName").type("Петров")
    browser.element("#userEmail").type("ivan@example.com")
    browser.element("#userNumber").type("1234567890")

    # 3. Выбрать пол (Radio button)
    browser.element(by.text("Male")).click()

    # 4. Выбрать дату рождения (пример для календаря)
    browser.element("#dateOfBirthInput").click()
    browser.element(".react-datepicker__month-select").type("May")
    browser.element(".react-datepicker__year-select").type("1990")
    browser.element(".react-datepicker__day--015").click()

    # 5. Выбрать предметы (Subjects)
    browser.element("#subjectsInput").type("Maths").press_enter()

    # 6. Выбрать хобби (Checkboxes)
    browser.element(by.text("Sports")).click()
    browser.element(by.text("Reading")).click()

    # 7. Загрузить файл
    browser.element("#uploadPicture").send_keys(
        os.path.abspath("test.txt")
    )  # Путь к файлу

    # 8. Заполнить адрес
    browser.element("#currentAddress").type("ул. Тестовая, 123")

    # 9. Скролл и выбор штата (с обработкой перекрытия)
    browser.element("#state").perform(command.js.scroll_into_view)
    browser.element("#state").click()
    browser.element(by.text("NCR")).click()

    # 10. Скролл и выбор города
    browser.element("#city").perform(command.js.scroll_into_view)
    browser.element("#city").click()
    browser.element(by.text("Delhi")).click()

    # 11. Отправить форму
    browser.element("#submit").press_enter()

    # 12. Проверить данные в модальном окне
    browser.element(".modal-content").should(be.visible)
    browser.element(".table").all("td").even.should(
        have.exact_texts(
            "Иван Петров",
            "ivan@example.com",
            "Male",
            "1234567890",
            "15 May,1990",
            "Maths",
            "Sports, Reading",
            "test.txt",
            "ул. Тестовая, 123",
            "NCR Delhi",
        )
    )

    # 13. Закрыть модальное окно
    browser.element("#closeLargeModal").click()
    browser.element(".modal-content").should(be.not_.visible)