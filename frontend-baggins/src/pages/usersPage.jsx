import { useState } from "react";
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
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
const data_popular = [{"second_item":499,"count":7},{"second_item":476,"count":2},{"second_item":92,"count":4}]
  
const UsersPage = () => {
    return (
        <div className="UsersPage">
            <h1>
                Общие тренды гостей
            </h1>
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
                            <PolarAngleAxis dataKey="second_item" fill="#111" stroke="#555" />
                        <PolarRadiusAxis /> 
                        <Radar
                            name="Mike"
                            dataKey="count"
                            stroke="#8884d8"
                            fill="#8884d8"
                            fillOpacity={0.6}
                        />
                        </RadarChart>
                        </Col>
                        
                    </Row>
                </div>
        </div>
    )
}

export default UsersPage;