import React, { memo, useState } from 'react'
import { Canvas } from '@react-three/fiber'
import { Grid, OrbitControls, Environment, GizmoHelper, GizmoViewport, Html, Text } from '@react-three/drei'
import { useControls } from 'leva'
import * as THREE from 'three'

const TowerPlot = ({ coordinates = [], elements = [] }) => {
  const [selectedNode, setSelectedNode] = useState(null)
  const [hoveredElement, setHoveredElement] = useState(null)
  const [selectedElement, setSelectedElement] = useState(null)


  const { gridSize, ...gridConfig } = useControls({
    gridSize: [10.5, 10.5],
    sectionSize: { value: 3.3, min: 0, max: 10, step: 0.1 },
    sectionThickness: { value: 1.5, min: 0, max: 5, step: 0.1 },
    sectionColor: '#575d9b',
    lineThickness: { value: 4, min: 1, max: 10, step: 1 },
    fadeDistance: { value: 25, min: 0, max: 100, step: 1 },
    fadeStrength: { value: 1, min: 0, max: 1, step: 0.1 },
    followCamera: false,
    infiniteGrid: true
  })

  const sphereRadius = 0.08
  const cylinderRadius = sphereRadius / 4.5

  return (
    <Canvas shadows camera={{ position: [0, 40, 40], fov: 25 }} style={{ height: '100%', width: '100%' }}>
      <Grid
        position={[0, 0, 0]}
        rotation={[0, 0, 0]}
        args={gridSize}
        sectionSize={gridConfig.sectionSize}
        sectionThickness={gridConfig.sectionThickness}
        sectionColor={gridConfig.sectionColor}
        fadeDistance={gridConfig.fadeDistance}
        fadeStrength={gridConfig.fadeStrength}
        followCamera={gridConfig.followCamera}
        infiniteGrid={true}
        renderOrder={0}
      />

      {/* Axis Labels */}
      <Text position={[2, 0, 0]} fontSize={0.5} color="red">X</Text>
      <Text position={[0, 2, 0]} fontSize={0.5} color="green">Y</Text>
      <Text position={[0, 0, 2]} fontSize={0.5} color="blue">Z</Text>

      <group position={[0, 0, 0]}>
        {/* Tower Elements as cylinders */}
        {elements.map((section, idx) => (
          <group key={`section-${idx}`}>
            {section.elements.map((el, i) => {
              const nodeStart = el.node_i
              const nodeEnd = el.node_j

              const startVec = new THREE.Vector3(...nodeStart)
              const endVec = new THREE.Vector3(...nodeEnd)
              const direction = new THREE.Vector3().subVectors(endVec, startVec)
              const length = direction.length()
              const position = new THREE.Vector3().addVectors(startVec, endVec).multiplyScalar(0.5)

              const quaternion = new THREE.Quaternion()
              quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), direction.clone().normalize())

              let color = idx % 2 === 0 ? '#ff0000' : '#ffffff' // 🔁 red/white alternation

              if (hoveredElement === `${idx}-${i}`) {
                color = '#00ffcc'
              }

              return (
                <mesh
                  key={`el-${idx}-${i}`}
                  position={position}
                  quaternion={quaternion}
                  renderOrder={2}
                  onPointerOver={() => setHoveredElement(`${idx}-${i}`)}
                  onPointerOut={() => setHoveredElement(null)}
                  onClick={(e) => {
                    e.stopPropagation()
                    setSelectedElement({ key: `${idx}-${i}`, length, position })
                  }}
                  
                >

                  <cylinderGeometry args={[cylinderRadius, cylinderRadius, length, 8]} />
                  {selectedElement?.key === `${idx}-${i}` && (
                    <Html distanceFactor={10} position={[0, 0, 0]} style={{ color: 'white', fontSize: '12px' }}>
                      Length: {selectedElement.length.toFixed(3)} m
                    </Html>
                  )}
                  <meshStandardMaterial color={color} depthTest={false} />
                </mesh>
              )
            })}
          </group>
        ))}

        {/* Tower Nodes as spheres */}
        {coordinates.map((coord, index) =>
          Object.entries(coord).map(([key, val]) =>
            Array.isArray(val) ? (
              <mesh
                key={`${index}-${key}`}
                position={[val[0], val[1], val[2]]}
                renderOrder={3}
                onClick={(e) => {
                  e.stopPropagation()
                  if (
                    selectedNode?.x === val[0] &&
                    selectedNode?.y === val[1] &&
                    selectedNode?.z === val[2]
                  ) {
                    setSelectedNode(null)
                  } else {
                    setSelectedNode({ x: val[0], y: val[1], z: val[2], key })
                  }
                }}
              >
                <sphereGeometry args={[sphereRadius, 8, 8]} />
                <meshStandardMaterial color="red" depthTest={false} />
                {selectedNode?.x === val[0] && selectedNode?.y === val[1] && selectedNode?.z === val[2] && (
                  <Html distanceFactor={10} style={{ pointerEvents: 'none', color: 'white', fontSize: '12px' }}>
                    {selectedNode.key} (
                    {selectedNode.x.toFixed(2)}, {selectedNode.y.toFixed(2)}, {selectedNode.z.toFixed(2)})
                  </Html>
                )}
              </mesh>
            ) : null
          )
        )}
      </group>

      <OrbitControls
        makeDefault
        enableRotate={true}
        enableZoom={true}
        enablePan={true}
        target={[0, 20, 0]}
      />

      <Environment preset="city" />

      <GizmoHelper alignment="bottom-right" margin={[80, 80]}>
        <GizmoViewport axisColors={['#ff4d4d', '#4dff4d', '#4d4dff']} labelColor="white" />
      </GizmoHelper>
    </Canvas>
  )
}

export default memo(TowerPlot)
