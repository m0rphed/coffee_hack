import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  Rectangle,
  ResponsiveContainer,
} from "recharts";

const data = [
  {
    name: "Page A",
    uv: 4000,
    pv: 2400,
    amt: 2400,
  },
  {
    name: "Page B",
    uv: 3000,
    pv: 1398,
    amt: 2210,
  },
  {
    name: "Page C",
    uv: 2000,
    pv: 9800,
    amt: 2290,
  },
  {
    name: "Page D",
    uv: 2780,
    pv: 3908,
    amt: 2000,
  },
  {
    name: "Page E",
    uv: 1890,
    pv: 4800,
    amt: 2181,
  },
  {
    name: "Page F",
    uv: 2390,
    pv: 3800,
    amt: 2500,
  },
  {
    name: "Page G",
    uv: 3490,
    pv: 4300,
    amt: 2100,
  },
];

const daa = [{"day_of_week_name":"Понедельник","count":120,"customer_id":9172},{"day_of_week_name":"Вторник","count":47,"customer_id":9172},{"day_of_week_name":"Среда","count":131,"customer_id":9172},{"day_of_week_name":"Четверг","count":146,"customer_id":9172},{"day_of_week_name":"Пятница","count":136,"customer_id":9172},{"day_of_week_name":"Суббота","count":37,"customer_id":9172},{"day_of_week_name":"Воскресенье","count":0,"customer_id":9172}]


export default function App() {
  return (
    <ResponsiveContainer width={"100%"} height={300}>
      <BarChart
        data={daa}
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
          fill="#B3CDAD"
          activeBar={<Rectangle fill="pink" stroke="blue" />}
        />
        
      </BarChart>
    </ResponsiveContainer>
  );
}
