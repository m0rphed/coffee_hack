import { useState } from "react";
import { Pane, Tablist, Tab, Paragraph } from 'evergreen-ui'
import { BarChart, Bar, Rectangle, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const data = [{"order_hour":12,"count":147,"customer_id":9172},{"order_hour":13,"count":116,"customer_id":9172},{"order_hour":14,"count":96,"customer_id":9172},{"order_hour":15,"count":64,"customer_id":9172},{"order_hour":11,"count":62,"customer_id":9172},{"order_hour":16,"count":49,"customer_id":9172},{"order_hour":17,"count":26,"customer_id":9172},{"order_hour":10,"count":22,"customer_id":9172},{"order_hour":18,"count":18,"customer_id":9172},{"order_hour":19,"count":7,"customer_id":9172},{"order_hour":9,"count":5,"customer_id":9172},{"order_hour":20,"count":4,"customer_id":9172},{"order_hour":21,"count":1,"customer_id":9172}]

const UsersPage = () => {
    const [selectedIndex, setSelectedIndex] = useState(0)
    const [tabs] = useState(['График 1', 'График 2', 'График 3'])
    const graph = {
        'График 1':graph1
    }
    return (
        <div className="UsersPage">
            <h1>
                Общие тренды гостей
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
                    <Paragraph>{graph[tab]}</Paragraph>
                </Pane>
                ))}
            </Pane>
            </Pane>
        </div>
    )
}

const graph1 = () => {
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
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="pv" fill="#8884d8" activeBar={<Rectangle fill="pink" stroke="blue" />} />
          <Bar dataKey="uv" fill="#82ca9d" activeBar={<Rectangle fill="gold" stroke="purple" />} />
        </BarChart>
      </ResponsiveContainer>
    )
}

export default UsersPage;