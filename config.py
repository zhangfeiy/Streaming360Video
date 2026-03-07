"""
Configuration file for OrbitStream 360-Degree Video Streaming Experiments

This module contains all configuration parameters for the simulation, including:
- Dataset paths and URLs
- Network simulation parameters  
- Video streaming parameters
- Homeostatic controller gains
- Gravitational field parameters
"""

import os
from dataclasses import dataclass, field
from typing import List, Dict

# ============================================================================
# Dataset Configuration
# ============================================================================

@dataclass
class DatasetConfig:
    """Configuration for 360-degree video datasets"""
    
    # Public 360 Video Datasets
    DATASETS = {
        # Head Movement Prediction Dataset from CVPR 2018
        # Paper: "Gaze prediction in dynamic 360 immersive videos"
        "xu2018gaze": {
            "name": "Xu et al. 360 Gaze Dataset",
            "url": "https://github.com/xuyanyu-shh/VR-EyeTracking/archive/refs/heads/master.zip",
            "description": "Head movement traces from 58 users watching 208 360-degree videos",
            "paper": "CVPR 2018",
            "size_mb": 150
        },
        # Saliency in VR Dataset  
        "saliency_vr": {
            "name": "Saliency in VR Dataset",
            "url": "https://github.com/phananh1010/PanoSalNet/archive/refs/heads/master.zip",
            "description": "Saliency maps for 360 video content",
            "paper": "MM 2018",
            "size_mb": 200
        },
        # David360 dataset - Public head tracking data
        "david360": {
            "name": "David360 Head Tracking",
            "url": "https://gitlab.com/music-project/david360-dataset/-/archive/master/david360-dataset-master.zip",
            "description": "360 video head tracking dataset",
            "paper": "QoMEX 2017",
            "size_mb": 50
        },
        # Network Traces Dataset
        "fcc_network": {
            "name": "FCC Broadband Speed Test Data",
            "url": "https://www.fcc.gov/oet/mba/raw-data-releases",
            "description": "Network throughput traces",
            "paper": "FCC MBA",
            "size_mb": 500
        }
    }
    
    # Local paths
    DATA_DIR: str = os.environ.get("STREAM360_DATA_ROOT", os.path.join(os.path.dirname(os.path.dirname(__file__)), "data"))
    RESULTS_DIR: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results")
    FIGURES_DIR: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "figures")

    # Synthetic data generation (fallback / augmentation)
    USE_SYNTHETIC_FALLBACK: bool = True
    SYNTHETIC_NETWORK_TRACES: int = 40
    SYNTHETIC_HEAD_TRACES: int = 20
    SYNTHETIC_TRACE_DURATION_SEC: float = 100.0
    SYNTHETIC_DIR_NAME: str = "synthetic_traces"
    SYNTHETIC_VIEWPORT_DIR_NAME: str = "synthetic_viewport"


# ============================================================================
# Network Simulation Parameters
# ============================================================================

@dataclass
class NetworkConfig:
    """Configuration for network channel simulation"""
    
    # 5G mmWave channel parameters
    MEAN_BANDWIDTH_MBPS: float = 20.0
    STD_BANDWIDTH_MBPS: float = 10.0
    MIN_BANDWIDTH_MBPS: float = 0.5
    MAX_BANDWIDTH_MBPS: float = 42.7
    
    # Fading model
    FADING_FREQUENCY: float = 0.1  # Hz
    FADING_AMPLITUDE: float = 10.0  # Mbps
    
    # Deep fade (blockage) events
    BLOCKAGE_PROBABILITY: float = 0.02  # per time step
    BLOCKAGE_DURATION_STEPS: int = 10
    BLOCKAGE_ATTENUATION: float = 0.1
    
    # Latency parameters
    BASE_LATENCY_MS: float = 20.0
    JITTER_STD_MS: float = 5.0


# ============================================================================
# Video Streaming Parameters
# ============================================================================

@dataclass  
class VideoConfig:
    """Configuration for 360-degree video streaming"""
    
    # Video encoding parameters
    RESOLUTION: str = "4K"  # 3840x1920
    FPS: int = 30
    SEGMENT_DURATION_SEC: float = 2.0  # 2-second chunks
    GOP_SIZE: int = 15  # Group of Pictures
    
    # Tile configuration (equirectangular projection)
    NUM_TILES_HORIZONTAL: int = 8
    NUM_TILES_VERTICAL: int = 4
    TOTAL_TILES: int = NUM_TILES_HORIZONTAL * NUM_TILES_VERTICAL
    
    # Quality levels (bitrates in Mbps)
    QUALITY_LEVELS: List[float] = field(default_factory=lambda: [1.2, 2.5, 5.0, 10.0, 20.0, 40.1])
    
    @property
    def QUALITY_LEVELS_MBPS(self) -> List[float]:
        return self.QUALITY_LEVELS
    
    # Viewport parameters
    VIEWPORT_WIDTH_DEG: float = 110.0  # degrees
    VIEWPORT_HEIGHT_DEG: float = 90.0  # degrees
    
    # Buffer parameters
    MAX_BUFFER_SEC: float = 10.0
    MIN_BUFFER_SEC: float = 0.5
    TARGET_BUFFER_SEC: float = 4.0


# ============================================================================
# Homeostatic Controller Parameters
# ============================================================================

@dataclass
class HomeostasisConfig:
    """Configuration for bio-inspired homeostatic rate controller"""
    
    # PD Controller gains
    K_P: float = 0.5   # Proportional gain (tonic response)
    K_D: float = 0.2   # Derivative gain (phasic response)
    
    # Adaptation parameters
    SMOOTHING_FACTOR: float = 0.7  # Low-pass filter for bitrate smoothing
    SAFETY_MARGIN: float = 0.9     # Conservative factor for bandwidth utilization

    # Tile allocation sharpness (>=1.0 concentrates more bitrate on likely tiles)
    ALLOCATION_SHARPNESS: float = 1.2
    
    # Saturation limits (biological constraints)
    MIN_ADAPTATION_RATE: float = 0.1
    MAX_ADAPTATION_RATE: float = 2.0
    
    # Stress response thresholds
    LOW_BUFFER_THRESHOLD: float = 1.0   # Trigger aggressive adaptation
    HIGH_BUFFER_THRESHOLD: float = 7.0  # Relax adaptation


# ============================================================================
# Gravitational Field Parameters  
# ============================================================================

@dataclass
class GravityConfig:
    """Configuration for physics-inspired gravitational viewport prediction"""
    
    # Universal constants
    GRAVITATIONAL_CONSTANT: float = 1.0  # Scaling factor G
    DECAY_EXPONENT: float = 1.0          # gamma in 1/r^gamma (use 1 for 1/(d + delta))
    POTENTIAL_DELTA: float = 1.0         # Regularization term in potential field
    
    # Attention temperature (for softmax)
    ATTENTION_BETA: float = 0.5  # Inverse attention temperature (T_att=2.0)
    
    # Semantic mass assignments (safety criticality)
    OBJECT_MASSES: Dict[str, float] = field(default_factory=lambda: {
        "pedestrian": 1.0,
        "cyclist": 0.9,
        "vehicle": 0.8,
        "traffic_sign": 0.7,
        "traffic_light": 0.85,
        "intersection": 0.75,
        "construction": 0.6,
        "lane_marking": 0.3,
        "background": 0.1
    })
    
    # Gaze inertia (how quickly gaze responds to gravity)
    GAZE_INERTIA: float = 0.8
    GAZE_NOISE_STD: float = 0.05


# ============================================================================
# Simulation Parameters
# ============================================================================

@dataclass
class SimulationConfig:
    """Configuration for simulation experiments"""
    
    # Time parameters
    DURATION_SEC: float = 100.0
    DT_SEC: float = 2.0  # Simulation time step (aligned with segment duration)
    
    # Random seed for reproducibility
    RANDOM_SEED: int = 42
    
    # Number of Monte Carlo runs
    NUM_RUNS: int = 300
    
    # Baseline algorithms to compare
    BASELINES: List[str] = field(default_factory=lambda: [
        "rate_based",      # Simple rate-based heuristic
        "buffer_based",    # Buffer-based algorithm (BBA)
        "mpc",             # Model Predictive Control
        "pensieve",        # DRL-based (Pensieve)
        "pano",            # Panoramic ABR
        "flare",           # FLARE algorithm
        "orbitstream"      # Our proposed method
    ])


# ============================================================================
# QoE Parameters
# ============================================================================

@dataclass
class QoEConfig:
    """Configuration for Quality of Experience metrics"""
    
    # QoE weights
    QUALITY_WEIGHT: float = 1.0
    REBUFFER_PENALTY: float = 10.0
    SMOOTHNESS_PENALTY: float = 0.5
    VIEWPORT_MISS_PENALTY: float = 5.0
    
    # Viewport accuracy threshold
    VIEWPORT_HIT_THRESHOLD_DEG: float = 30.0


# ============================================================================
# Combined Configuration
# ============================================================================

@dataclass
class Config:
    """Master configuration combining all sub-configurations"""
    
    dataset: DatasetConfig = field(default_factory=DatasetConfig)
    network: NetworkConfig = field(default_factory=NetworkConfig)
    video: VideoConfig = field(default_factory=VideoConfig)
    homeostasis: HomeostasisConfig = field(default_factory=HomeostasisConfig)
    gravity: GravityConfig = field(default_factory=GravityConfig)
    simulation: SimulationConfig = field(default_factory=SimulationConfig)
    qoe: QoEConfig = field(default_factory=QoEConfig)


# Create default configuration instance
DEFAULT_CONFIG = Config()


if __name__ == "__main__":
    # Print configuration summary
    config = Config()
    print("=" * 60)
    print("OrbitStream Configuration Summary")
    print("=" * 60)
    print(f"\nSimulation Duration: {config.simulation.DURATION_SEC}s")
    print(f"Time Step: {config.simulation.DT_SEC}s")
    print(f"Number of Runs: {config.simulation.NUM_RUNS}")
    print(f"\nNetwork:")
    print(f"  Mean Bandwidth: {config.network.MEAN_BANDWIDTH_MBPS} Mbps")
    print(f"  Std Bandwidth: {config.network.STD_BANDWIDTH_MBPS} Mbps")
    print(f"\nVideo:")
    print(f"  Resolution: {config.video.RESOLUTION}")
    print(f"  Tiles: {config.video.NUM_TILES_HORIZONTAL}x{config.video.NUM_TILES_VERTICAL}")
    print(f"  Quality Levels: {config.video.QUALITY_LEVELS}")
    print(f"\nHomeostatic Controller:")
    print(f"  Kp: {config.homeostasis.K_P}, Kd: {config.homeostasis.K_D}")
    print(f"  Target Buffer: {config.video.TARGET_BUFFER_SEC}s")
    print(f"\nGravitational Field:")
    print(f"  G: {config.gravity.GRAVITATIONAL_CONSTANT}")
    print(f"  Decay: 1/r^{config.gravity.DECAY_EXPONENT}")
    print(f"  Object Masses: {config.gravity.OBJECT_MASSES}")
