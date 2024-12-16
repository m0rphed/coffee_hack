import { useEffect, useState } from "react";
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Button from 'react-bootstrap/Button';
import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
    ResponsiveContainer,
    LabelList,
    ComposedChart,
    Bar,
    BarChart,
    Rectangle,
    PieChart, 
    Pie,
    Radar,
    RadarChart,
    PolarGrid,
    PolarAngleAxis,
    PolarRadiusAxis,
  } from "recharts";


const data_hours = [{"order_hour":12,"count":147,"customer_id":9172},{"order_hour":13,"count":116,"customer_id":9172},{"order_hour":14,"count":96,"customer_id":9172},{"order_hour":15,"count":64,"customer_id":9172},{"order_hour":11,"count":62,"customer_id":9172},{"order_hour":16,"count":49,"customer_id":9172},{"order_hour":17,"count":26,"customer_id":9172},{"order_hour":10,"count":22,"customer_id":9172},{"order_hour":18,"count":18,"customer_id":9172},{"order_hour":19,"count":7,"customer_id":9172},{"order_hour":9,"count":5,"customer_id":9172},{"order_hour":20,"count":4,"customer_id":9172},{"order_hour":21,"count":1,"customer_id":9172}]
const data_week = [{"day_of_week_name":"Понедельник","count":120,"customer_id":9172},{"day_of_week_name":"Вторник","count":47,"customer_id":9172},{"day_of_week_name":"Среда","count":131,"customer_id":9172},{"day_of_week_name":"Четверг","count":146,"customer_id":9172},{"day_of_week_name":"Пятница","count":136,"customer_id":9172},{"day_of_week_name":"Суббота","count":37,"customer_id":9172},{"day_of_week_name":"Воскресенье","count":0,"customer_id":9172}]
const data_popular = [{"entity_id":585,"order_count":45,"customer_id":9172},{"entity_id":541,"order_count":43,"customer_id":9172},{"entity_id":542,"order_count":26,"customer_id":9172},{"entity_id":536,"order_count":22,"customer_id":9172},{"entity_id":350,"order_count":21,"customer_id":9172},{"entity_id":1206,"order_count":19,"customer_id":9172},{"entity_id":238,"order_count":19,"customer_id":9172},{"entity_id":584,"order_count":16,"customer_id":9172},{"entity_id":406,"order_count":15,"customer_id":9172},{"entity_id":835,"order_count":15,"customer_id":9172}]
const order_sale = [{"second_item":499,"count":7},{"second_item":476,"count":2},{"second_item":92,"count":4}]

const OneUserPage = () => {
    const [data_hours, Setdata_hours] = useState([])
    const [data_week, Setdata_week] = useState([])
    const [data_popular, Setdata_popular] = useState([])
    const [order_sale, Setorder_sale] = useState([])
    const [user_id, setUserID] = useState(9172)
    const [enable_id, setEnableID] = useState(0)

    const getApi_data_hours = async () => {
        const response = await fetch(
          "http://158.255.6.113:8000/customer/time_of_day_preference/" + user_id
        ).then((response) => response.json());
      
        // Обновим состояние
        Setdata_hours(response);
      };
      const getApi_data_week = async () => {
        const response = await fetch(
          "http://158.255.6.113:8000/customer/time_of_day_preference/" + user_id
        ).then((response) => response.json());
      
        // Обновим состояние
        Setdata_week(response);
      };
      const getApi_data_popular = async () => {
        const response = await fetch(
          "http://158.255.6.113:8000/customer/time_of_day_preference/" + user_id
        ).then((response) => response.json());
      
        // Обновим состояние
        Setdata_popular(response);
      };

      useEffect(() => {
        getApi_data_hours();
      }, [user_id]);




    
    return (
        <div className="OneUserPage">
            <h1>
                Конкретный гость
            </h1>
            <div className="Main__container">
                <Form className="Graph_input">
                    <Row>
                        <Col>
                            <Form.Group className="mb-3">
                                <Form.Label>Введите id клиента </Form.Label>
                                <Form.Control type="text" name="id_user" placeholder="123456" size="lg" onChange={e => setUserID(e)}/>
                            </Form.Group>
                            <Button  variant="primary" type="submit" onClick={e => {}}>
                                Получить данные
                            </Button>
                        </Col>
                        <Col>
                        </Col>
                        <Col>
                            <Form.Group className="mb-3">
                                <Form.Label>Введите id товара </Form.Label>
                                <Form.Control type="text" name="id_user" placeholder="123456" size="lg" onChange={e => setEnableID(e)}/>
                            </Form.Group>
                            <Button  variant="primary" type="submit" onClick={e => {}}>
                                Получить данные
                            </Button>
                        </Col>
                        <Col>
                        </Col>
                    </Row>
                </Form>
                <div className="Graph__container">
                    <Row>
                        <Col>
                        <h4 className="Graph__header">
                            Частота посещения пользователя по времени
                        </h4>
                        <ResponsiveContainer width={"100%"} height={400}>
                            <LineChart data={data_hours} margin={{ top: 20 }}>
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey="order_hour" padding={{ left: 30, right: 30 }} />
                                <YAxis />
                                <Tooltip />
                                <Legend />
                                <Line
                                type="monotone"
                                dataKey="count"
                                stroke="#8884d8"
                                activeDot={{ r: 8 }}
                                >
                                <LabelList position="top" offset={10} />
                                </Line>
                            </LineChart>
                        </ResponsiveContainer>
                        </Col>
                        <Col>
                        <h4 className="Graph__header">
                            Персональная скидка пользователя к покупке
                        </h4>
                        <RadarChart
                        cx={300}
                        cy={250}
                        outerRadius={150}
                        width={500}
                        height={500}
                        data={order_sale}
                        
                        >
                        <PolarGrid stroke="#111" /> 
                            <PolarAngleAxis dataKey="second_item" fill="#111" stroke="#555" />
                        <PolarRadiusAxis /> 
                        <Radar
                            name="Mike"
                            dataKey="count"
                            stroke="#dc0087"
                            fill="#dc0087"
                            fillOpacity={0.6}
                        />
                        </RadarChart>
                        </Col>
                    </Row>
                    <Row>
                    <Col>
                        <h4 className="Graph__header">
                            Частота посещения пользователя по дню недели
                        </h4>
                        <ResponsiveContainer width={"100%"} height={400}>
                            <BarChart
                                data={data_week}
                                margin={{
                                top: 5,
                                right: 30,
                                left: 20,
                                bottom: 5,
                                }}
                            >
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey="day_of_week_name" />
                                <YAxis />
                                <Tooltip />
                                <Bar
                                dataKey="count"
                                fill="#FF5F5E"
                                activeBar={<Rectangle fill="gold" stroke="purple" />}
                                barSize={30}
                                />
                            </BarChart>
                        </ResponsiveContainer>
                        </Col>
                        <Col>
                        <h4 className="Graph__header">
                            Любимые продукты пользователя
                        </h4>
                        <RadarChart
                        cx={300}
                        cy={250}
                        outerRadius={150}
                        width={500}
                        height={500}
                        data={data_popular}
                        
                        >
                        <PolarGrid stroke="#111" /> 
                            <PolarAngleAxis dataKey="entity_id" fill="#111" stroke="#555" />
                        <PolarRadiusAxis /> 
                        <Radar
                            name="Mike"
                            dataKey="order_count"
                            stroke="#8884d8"
                            fill="#8884d8"
                            fillOpacity={0.6}
                        />
                        </RadarChart>
                        </Col>
                        
                    </Row>
                </div>
            </div>
        </div>
    )
}

export default OneUserPage;