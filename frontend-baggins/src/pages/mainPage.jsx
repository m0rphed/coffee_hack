import {
  Card,
  CardBody,
  CardFooter,
  CardHeader,
} from "grommet";
import coffee from "../images/coffee-cup.png"
import users from "../images/group.png"
import analitics from "../images/analitics.png"


const MainPage_1 = () => {
    
    return (
      <div className="MainPage">
        <Card  height="medium" width="medium" background="light-1">
          <CardHeader pad="medium">Отчёт для отдела маркетинга</CardHeader>
          <CardBody pad="medium">
            <div>
              <img src={analitics} width="255px"></img>
            </div>
          </CardBody>
          <a href="/analis">
            <CardFooter pad="medium" background="light-2">
              Ссылка
            </CardFooter>
          </a>
        </Card>
        <Card  height="medium" width="medium" background="light-1">
          <CardHeader pad="medium">Общие тренды гостей</CardHeader>
          <CardBody pad="medium"><img src={users} width="255px" height="255px"></img></CardBody>
          <a href="/users">
            <CardFooter pad="medium" background="light-2">
              Ссылка
            </CardFooter>
          </a>
        </Card>
        <Card  height="medium" width="medium" background="light-1">
          <CardHeader pad="medium">Конкретный гость</CardHeader>
          <CardBody pad="medium"><img src={coffee}></img></CardBody>
          <a href="/oneuser">
            <CardFooter pad="medium" background="light-2">
              Ссылка
            </CardFooter>
          </a>
        </Card>
      </div>
    )
}

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


