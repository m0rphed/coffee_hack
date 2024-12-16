import { useState } from "react";
import { Pane, Tablist, Tab, Paragraph } from 'evergreen-ui'
import { BarChart, Bar, Rectangle, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const daa = [{"day_of_week_name":"Понедельник","count":120,"customer_id":9172},{"day_of_week_name":"Вторник","count":47,"customer_id":9172},{"day_of_week_name":"Среда","count":131,"customer_id":9172},{"day_of_week_name":"Четверг","count":146,"customer_id":9172},{"day_of_week_name":"Пятница","count":136,"customer_id":9172},{"day_of_week_name":"Суббота","count":37,"customer_id":9172},{"day_of_week_name":"Воскресенье","count":0,"customer_id":9172}]

const data = [
    {
      name: 'Page A',
      uv: 4000,
      pv: 2400,
      amt: 2400,
    },
    {
      name: 'Page B',
      uv: 3000,
      pv: 1398,
      amt: 2210,
    },
    {
      name: 'Page C',
      uv: 2000,
      pv: 9800,
      amt: 2290,
    },
    {
      name: 'Page D',
      uv: 2780,
      pv: 3908,
      amt: 2000,
    },
    {
      name: 'Page E',
      uv: 1890,
      pv: 4800,
      amt: 2181,
    },
    {
      name: 'Page F',
      uv: 2390,
      pv: 3800,
      amt: 2500,
    },
    {
      name: 'Page G',
      uv: 3490,
      pv: 4300,
      amt: 2100,
    },
  ];

const Graph1 = () => {
    return (
        <ResponsiveContainer width="100%" height="100%">
        <BarChart
          width={500}
          height={300}
          data={data}
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
          <Legend />
          <Bar dataKey="count" fill="#8884d8" activeBar={<Rectangle fill="pink" stroke="blue" />} />
        </BarChart>
      </ResponsiveContainer>
    )
}

const AnalisPage = () => {
    const [selectedIndex, setSelectedIndex] = useState(0)
    const [tabs] = useState(['График 1', 'График 2', 'График 3'])
    const [graph] = useState(['<graph1/>', 'График 2', 'График 3'])
    return (
        <div className="AnalisPage">
            <h1>
                Отчёт для отдела маркетинга
            </h1>
            <Pane height={120}>
            <Tablist marginBottom={16} flexBasis={240} marginRight={24}>
                {tabs.map((tab, index) => (
                <Tab
                    aria-controls={`panel-${tab}`}
                    isSelected={index === selectedIndex}
                    key={tab}
                    onSelect={() => setSelectedIndex(index)}
                >
                    {tab}
                </Tab>
                ))}
            </Tablist>
            <Pane padding={16} background="tint1" flex="1">
                {tabs.map((tab, index) => (
                <Pane
                    aria-labelledby={tab}
                    aria-hidden={index !== selectedIndex}
                    display={index === selectedIndex ? 'block' : 'none'}
                    key={tab}
                    role="tabpanel"
                >
                    <Paragraph>
                    <ResponsiveContainer width="100%" height="100%">
                        <BarChart
                        width={500}
                        height={300}
                        data={data}
                        margin={{
                            top: 5,
                            right: 30,
                            left: 20,
                            bottom: 5,
                        }}
                        >
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="name" />
                        <YAxis />
                        <Tooltip />
                        <Legend />
                        <Bar dataKey="pv" fill="#8884d8" activeBar={<Rectangle fill="pink" stroke="blue" />} />
                        <Bar dataKey="uv" fill="#82ca9d" activeBar={<Rectangle fill="gold" stroke="purple" />} />
                        </BarChart>
                    </ResponsiveContainer>
                    </Paragraph>
                </Pane>
                ))}
            </Pane>
            </Pane> 
        </div>
    )
}

export default AnalisPage;