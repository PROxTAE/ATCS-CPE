/**
 * guitar3d.js - Loads and Renders the User's Real 3D Electric Guitar Model (gu.obj) with High-Res PBR Textures
 * Full WebGL 3D Interactive: Textures (Maple, Sunburst, Obsidian Lacquer, Chrome, Pearl), 360° Orbit, Zoom, Hotspots.
 */

let scene, camera, renderer, controls, guitarGroup;
let isAutoRotating = true;
let isWireframe = false;
let loadedGuitarMesh = null;
let currentFinish = "obsidian"; // 'obsidian' | 'sunburst' | 'maple'

// Material references for dynamic finish swapping
let bodyMaterial, mapleMaterial, chromeMaterial, pickguardMaterial;

// 3D Hotspot anchors mapped to enlarged gu.obj coordinate space
const HOTSPOT_ANCHORS = {
  headstock: new THREE.Vector3(10.2, 3.2, 0.4),
  neck: new THREE.Vector3(4.2, 1.2, 0.3),
  body: new THREE.Vector3(-4.8, -1.2, 2.2),
  pickups: new THREE.Vector3(-1.8, 0.5, 0.2),
  bridge: new THREE.Vector3(-5.2, 0.4, 0.2),
  tone: new THREE.Vector3(-3.8, -0.6, -2.2)
};

// Texture Loader
const textureLoader = new THREE.TextureLoader();

// Load Textures
const mapleTexture = textureLoader.load("/static/textures/maple_wood.jpg");
mapleTexture.wrapS = THREE.RepeatWrapping;
mapleTexture.wrapT = THREE.RepeatWrapping;
mapleTexture.repeat.set(2, 4);

const bodyLacquerTexture = textureLoader.load("/static/textures/body_lacquer.jpg");
bodyLacquerTexture.wrapS = THREE.RepeatWrapping;
bodyLacquerTexture.wrapT = THREE.RepeatWrapping;
bodyLacquerTexture.repeat.set(3, 3);

const sunburstTexture = textureLoader.load("/static/textures/sunburst_body.jpg");

const chromeTexture = textureLoader.load("/static/textures/chrome_metal.jpg");
chromeTexture.wrapS = THREE.RepeatWrapping;
chromeTexture.wrapT = THREE.RepeatWrapping;
chromeTexture.repeat.set(2, 2);

const pearlTexture = textureLoader.load("/static/textures/pearl_pickguard.jpg");
pearlTexture.wrapS = THREE.RepeatWrapping;
pearlTexture.wrapT = THREE.RepeatWrapping;
pearlTexture.repeat.set(4, 4);

function init3DGuitar() {
  const container = document.getElementById("guitar-canvas-container");
  const canvas = document.getElementById("guitar-3d-canvas");

  if (!container || !canvas) return;

  const width = container.clientWidth || 600;
  const height = container.clientHeight || 340;

  // 1. Scene
  scene = new THREE.Scene();

  // 2. Camera setup for Wide Cinematic Perspective
  camera = new THREE.PerspectiveCamera(34, width / height, 0.1, 1000);
  camera.position.set(0.5, 1.5, 16.5);

  // 3. WebGL Renderer
  renderer = new THREE.WebGLRenderer({
    canvas: canvas,
    antialias: true,
    alpha: true,
    powerPreference: "high-performance"
  });
  renderer.setSize(width, height);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.setClearColor(0x000000, 0); // Pure transparent black
  renderer.outputEncoding = THREE.sRGBEncoding;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.45;

  // 4. OrbitControls
  controls = new THREE.OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.06;
  controls.enableZoom = true;
  controls.minDistance = 5;
  controls.maxDistance = 35;
  controls.autoRotate = true;
  controls.autoRotateSpeed = 1.0;

  // 5. Studio Lighting Setup (Enhanced Cinematic Rim & Cyberpunk Glows)
  const ambientLight = new THREE.AmbientLight(0xffffff, 1.05);
  scene.add(ambientLight);

  const keyLight = new THREE.DirectionalLight(0xffeedd, 3.0);
  keyLight.position.set(-6, 14, 12);
  scene.add(keyLight);

  const rimLight = new THREE.DirectionalLight(0xff6600, 4.8);
  rimLight.position.set(10, 6, -8);
  scene.add(rimLight);

  const fillLight = new THREE.PointLight(0xff5500, 3.5, 40);
  fillLight.position.set(-2, -4, 6);
  scene.add(fillLight);

  const headLight = new THREE.PointLight(0xffaa44, 2.5, 30);
  headLight.position.set(8, 4, 5);
  scene.add(headLight);

  // 6. Guitar Root Group
  guitarGroup = new THREE.Group();
  scene.add(guitarGroup);

  // 7. Setup Materials with Textures
  setupMaterials();

  // 8. Load User's OBJ 3D Model (gu.obj)
  loadUserGuitarModel();

  // 9. Setup HUD Button Controls
  setup3DButtons();

  // 10. Resize Listener
  window.addEventListener("resize", onWindowResize);

  // 11. Start Animation Loop
  animate();
}

function setupMaterials() {
  // Obsidian Glossy Body Material with Lacquer / Carbon Texture
  bodyMaterial = new THREE.MeshPhysicalMaterial({
    map: bodyLacquerTexture,
    color: 0x24242c,
    metalness: 0.22,
    roughness: 0.14,
    clearcoat: 1.0,
    clearcoatRoughness: 0.04,
    reflectivity: 0.98
  });

  // Maple Wood Grain Material for Neck & Fretboard
  mapleMaterial = new THREE.MeshStandardMaterial({
    map: mapleTexture,
    color: 0xffddaa,
    roughness: 0.42,
    metalness: 0.05,
    bumpMap: mapleTexture,
    bumpScale: 0.02
  });

  // Polished Chrome Metal Material for Pickups & Hardware
  chromeMaterial = new THREE.MeshStandardMaterial({
    map: chromeTexture,
    color: 0xffffff,
    metalness: 0.98,
    roughness: 0.1
  });

  // Pearl Pickguard Material
  pickguardMaterial = new THREE.MeshStandardMaterial({
    map: pearlTexture,
    color: 0xffffee,
    roughness: 0.25,
    metalness: 0.05
  });
}

function loadUserGuitarModel() {
  const loader = new THREE.OBJLoader();

  loader.load(
    "/static/models/gu.obj",
    (obj) => {
      // Compute Bounding Box to Center and Normalize Scale
      const box = new THREE.Box3().setFromObject(obj);
      const center = box.getCenter(new THREE.Vector3());
      const size = box.getSize(new THREE.Vector3());

      // Center geometry at (0, 0, 0)
      obj.position.x = -center.x;
      obj.position.y = -center.y;
      obj.position.z = -center.z;

      // Assign PBR materials based on mesh characteristics
      obj.traverse((child) => {
        if (child.isMesh) {
          child.castShadow = true;
          child.receiveShadow = true;

          const name = (child.name || "").toLowerCase();
          const pName = (child.parent ? child.parent.name : "").toLowerCase();
          const combined = name + " " + pName;

          if (combined.includes("guard") || combined.includes("plate") || combined.includes("white")) {
            child.material = pickguardMaterial;
          } else if (combined.includes("neck") || combined.includes("fretboard") || combined.includes("head") || combined.includes("wood")) {
            child.material = mapleMaterial;
          } else if (combined.includes("chrome") || combined.includes("pickup") || combined.includes("bridge") || combined.includes("string") || combined.includes("tuner") || combined.includes("knob") || combined.includes("metal")) {
            child.material = chromeMaterial;
          } else {
            // Default body lacquer finish
            child.material = bodyMaterial;
          }
        }
      });

      const wrapper = new THREE.Group();
      wrapper.add(obj);

      // Scale model larger for full-bleed overlapping cinematic presence (scale ~23.5)
      const maxDim = Math.max(size.x, size.y, size.z);
      const scaleFactor = 23.5 / (maxDim || 30.0);
      wrapper.scale.set(scaleFactor, scaleFactor, scaleFactor);

      // Rotate dynamically: body towards left-center, neck stretching across to top-right
      wrapper.rotation.x = -Math.PI / 2 + 0.12;
      wrapper.rotation.z = 0.28;
      wrapper.position.set(0.8, -0.2, 0);

      guitarGroup.add(wrapper);
      loadedGuitarMesh = wrapper;

      console.log("🎸 Loaded 3D Guitar Model in Giant Overlapping Cinematic View!");
    },
    (xhr) => {
      if (xhr.lengthComputable) {
        const percent = Math.round((xhr.loaded / xhr.total) * 100);
        const hintBadge = document.querySelector(".three-hint-badge");
        if (hintBadge && percent < 100) {
          hintBadge.innerHTML = `<i class="fa-solid fa-spinner fa-spin orange-text"></i> Loading 3D Model & Textures (${percent}%)...`;
        } else if (hintBadge && percent >= 100) {
          hintBadge.innerHTML = `<i class="fa-solid fa-hand-pointer orange-text"></i> Drag to Rotate 360° · Scroll to Zoom · Click Hotspots`;
        }
      }
    },
    (err) => {
      console.error("Error loading gu.obj:", err);
    }
  );
}

// ================= 3D HUD HOTSPOT PROJECTIONS =================
function updateHotspotProjections() {
  const container = document.getElementById("guitar-canvas-container");
  if (!container || !camera) return;

  const width = container.clientWidth;
  const height = container.clientHeight;

  for (const [key, localPos] of Object.entries(HOTSPOT_ANCHORS)) {
    const el = document.getElementById(`hp-${key}`);
    if (!el) continue;

    const worldPos = localPos.clone();
    guitarGroup.localToWorld(worldPos);

    const screenPos = worldPos.clone().project(camera);

    if (screenPos.z > 1) {
      el.style.display = "none";
      continue;
    }

    const x = (screenPos.x * 0.5 + 0.5) * width;
    const y = (-(screenPos.y * 0.5) + 0.5) * height;

    el.style.display = "flex";
    el.style.left = `${x}px`;
    el.style.top = `${y}px`;
  }
}

// ================= CONTROLS & EVENT LISTENERS =================
function setup3DButtons() {
  const btnRotate = document.getElementById("btn-3d-rotate");
  const btnWireframe = document.getElementById("btn-3d-wireframe");
  const btnReset = document.getElementById("btn-3d-reset");
  const btnFinish = document.getElementById("btn-3d-finish");

  if (btnRotate) {
    btnRotate.addEventListener("click", () => {
      isAutoRotating = !isAutoRotating;
      controls.autoRotate = isAutoRotating;
      btnRotate.classList.toggle("active", isAutoRotating);
    });
  }

  if (btnWireframe) {
    btnWireframe.addEventListener("click", () => {
      isWireframe = !isWireframe;
      if (guitarGroup) {
        guitarGroup.traverse((child) => {
          if (child.isMesh && child.material) {
            child.material.wireframe = isWireframe;
          }
        });
      }
      btnWireframe.classList.toggle("active", isWireframe);
    });
  }

  if (btnFinish) {
    btnFinish.addEventListener("click", () => {
      // Toggle finish between Obsidian and Sunburst
      if (currentFinish === "obsidian") {
        currentFinish = "sunburst";
        bodyMaterial.map = sunburstTexture;
        bodyMaterial.color.setHex(0xffffff);
        bodyMaterial.needsUpdate = true;
        btnFinish.innerHTML = '<i class="fa-solid fa-palette"></i> SUNBURST';
      } else {
        currentFinish = "obsidian";
        bodyMaterial.map = bodyLacquerTexture;
        bodyMaterial.color.setHex(0x222228);
        bodyMaterial.needsUpdate = true;
        btnFinish.innerHTML = '<i class="fa-solid fa-palette"></i> OBSIDIAN';
      }
    });
  }

  if (btnReset) {
    btnReset.addEventListener("click", () => {
      controls.reset();
      camera.position.set(0, 4, 18);
      if (loadedGuitarMesh) {
        loadedGuitarMesh.rotation.set(-Math.PI / 2 + 0.15, 0, 0.2);
      }
    });
  }
}

function onWindowResize() {
  const container = document.getElementById("guitar-canvas-container");
  if (!container || !renderer || !camera) return;

  const width = container.clientWidth;
  const height = container.clientHeight;

  camera.aspect = width / height;
  camera.updateProjectionMatrix();
  renderer.setSize(width, height);
}

function animate() {
  requestAnimationFrame(animate);

  controls.update();
  updateHotspotProjections();
  renderer.render(scene, camera);
}

// Start on DOM ready
document.addEventListener("DOMContentLoaded", () => {
  setTimeout(init3DGuitar, 100);
});
