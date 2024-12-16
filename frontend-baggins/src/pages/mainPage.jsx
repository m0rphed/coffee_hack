import coffee from "../images/coffee-cup.png"
import users from "../images/group.png"
import analitics from "../images/analitics.png"

const MainPage = () => {
  const cards = [
    {
      "header":"Отчёт для отдела маркетинга",
      "img":analitics,
      "link":"/analis"
    },
    {
      "header":"Общие тренды гостей",
      "img":users,
      "link":"/users"
    },
    {
      "header":"Конкретный гость",
      "img":coffee,
      "link":"/oneuser"
    }
  ]
  return (
    <div className="MainPage">
      {cards.map(elem => 
        <div className="Card">
          <div className="Card__header">
            <h3 className="Card_h3">
              {elem.header}
            </h3>
          </div>
        <div className="Card__body">
          <img src={elem.img} className="Card_img"></img>
        </div>
        <div className="Card__footer">
          <a href={elem.link} className="Card__link">
            <div className="Card__linktext">К анализу!</div>
          </a>
        </div>
        </div>
      )}
    </div>
  )
}

export default MainPage;


