import { useState } from "react";
import { Pane, Tablist, Tab, Paragraph } from 'evergreen-ui'

const AnalisPage = () => {
    const [selectedIndex, setSelectedIndex] = useState(0)
    const [tabs] = useState(['График 1', 'График 2', 'График 3'])
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
                    <Paragraph>Описание и сам {tab}</Paragraph>
                </Pane>
                ))}
            </Pane>
            </Pane> 
        </div>
    )
}

export default AnalisPage;