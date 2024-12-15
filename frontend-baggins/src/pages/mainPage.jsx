import {
  Card,
  CardBody,
  CardFooter,
  CardHeader,
} from "grommet";
import coffee from "../images/coffee-cup.png"
import users from "../images/group.png"
import analitics from "../images/analitics.png"


const MainPage = () => {
    
    return (
      <div className="MainPage">
        <Card  height="medium" width="medium" background="light-1">
          <CardHeader pad="medium">Отчёт для отдела маркетинга</CardHeader>
          <CardBody pad="medium">
            <img src={analitics} width="255px"></img>
          </CardBody>
          <a href="/analis">
            <CardFooter pad="medium" background="light-2">
              Ссылка
            </CardFooter>
          </a>
        </Card>
        <Card  height="medium" width="medium" background="light-1">
          <CardHeader pad="medium">Общие тренды гостей</CardHeader>
          <CardBody pad="medium"><img src={users}></img></CardBody>
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

export default MainPage;


