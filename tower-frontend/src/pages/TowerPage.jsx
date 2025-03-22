import React, { useEffect, useState } from "react";
import { getTowerData } from "../services/api";
import Tower3D from "../components/Tower3D";

const TowerPage = ({ towerId }) => {
    const [towerData, setTowerData] = useState(null);

    useEffect(() => {
        getTowerData(towerId).then(setTowerData);
    }, [towerId]);

    return (
        <div>
            <h1>Tower ID: {towerId}</h1>
            {towerData ? (
                <>
                    <pre>{JSON.stringify(towerData, null, 2)}</pre>
                    <Tower3D towerData={towerData} />
                </>
            ) : (
                <p>Loading tower data...</p>
            )}
        </div>
    );
};

export default TowerPage;
