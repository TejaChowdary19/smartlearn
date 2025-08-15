"""
Multimodal integration for SmartLearn AI.
Handles image, audio, and video processing and generation.
"""

import os
import json
import base64
from typing import List, Dict, Any, Optional, Tuple, Union
from dataclasses import dataclass
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cv2
import torch
from transformers import (
    VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer,
    AutoProcessor, AutoModelForVision2Seq,
    pipeline
)

# Optional imports with fallbacks
try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False
    print("⚠️ Whisper not available - audio transcription will be limited")

try:
    from moviepy.editor import VideoFileClip, AudioFileClip
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False
    print("⚠️ MoviePy not available - video processing will be limited")

try:
    import librosa
    LIBROSA_AVAILABLE = True
except ImportError:
    LIBROSA_AVAILABLE = False
    print("⚠️ Librosa not available - audio analysis will be limited")

try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    PLOTTING_AVAILABLE = True
except ImportError:
    PLOTTING_AVAILABLE = False
    print("⚠️ Matplotlib/Seaborn not available - plotting will be limited")

@dataclass
class MultimodalContent:
    """Represents multimodal content with metadata."""
    content_type: str  # "image", "audio", "video", "text"
    content: Any
    metadata: Dict[str, Any]
    source: str
    timestamp: str

class ImageProcessor:
    """Handles image processing and analysis."""
    
    def __init__(self):
        self.image_processor = None
        self.image_model = None
        self.caption_model = None
        self.caption_tokenizer = None
        self._load_models()
    
    def _load_models(self):
        """Load image processing models."""
        try:
            # Load image captioning model
            model_name = "nlpconnect/vit-gpt2-image-captioning"
            self.caption_model = VisionEncoderDecoderModel.from_pretrained(model_name)
            self.caption_tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.image_processor = ViTImageProcessor.from_pretrained(model_name)
            print("✅ Image models loaded successfully")
        except Exception as e:
            print(f"⚠️ Warning: Could not load image models: {e}")
            print("Image processing will be limited")
    
    def process_image(self, image_path: str) -> MultimodalContent:
        """Process an image and extract information."""
        try:
            # Load image
            image = Image.open(image_path)
            
            # Generate caption
            caption = self._generate_caption(image)
            
            # Extract text using OCR (if available)
            extracted_text = self._extract_text_from_image(image)
            
            # Analyze image content
            analysis = self._analyze_image_content(image)
            
            metadata = {
                "caption": caption,
                "extracted_text": extracted_text,
                "analysis": analysis,
                "size": image.size,
                "mode": image.mode,
                "format": image.format
            }
            
            return MultimodalContent(
                content_type="image",
                content=image,
                metadata=metadata,
                source=image_path,
                timestamp=self._get_timestamp()
            )
            
        except Exception as e:
            print(f"❌ Error processing image {image_path}: {e}")
            return None
    
    def _generate_caption(self, image: Image.Image) -> str:
        """Generate a caption for the image."""
        if not self.caption_model:
            return "Image processing not available"
        
        try:
            # Preprocess image
            pixel_values = self.image_processor(image, return_tensors="pt").pixel_values
            
            # Generate caption
            with torch.no_grad():
                output_ids = self.caption_model.generate(
                    pixel_values,
                    max_length=50,
                    num_beams=4,
                    return_dict_in_generate=True
                ).sequences
            
            caption = self.caption_tokenizer.batch_decode(output_ids, skip_special_tokens=True)[0]
            return caption.strip()
            
        except Exception as e:
            print(f"Error generating caption: {e}")
            return "Could not generate caption"
    
    def _extract_text_from_image(self, image: Image.Image) -> str:
        """Extract text from image using OCR."""
        try:
            import pytesseract
            text = pytesseract.image_to_string(image)
            return text.strip()
        except Exception as e:
            return ""
    
    def _analyze_image_content(self, image: Image.Image) -> Dict[str, Any]:
        """Analyze image content and characteristics."""
        analysis = {}
        
        # Convert to numpy array for analysis
        img_array = np.array(image)
        
        # Basic statistics
        analysis["dimensions"] = img_array.shape
        analysis["data_type"] = str(img_array.dtype)
        
        # Color analysis
        if len(img_array.shape) == 3:  # Color image
            analysis["channels"] = img_array.shape[2]
            analysis["color_space"] = "RGB" if img_array.shape[2] == 3 else "RGBA"
            
            # Calculate average colors
            avg_colors = np.mean(img_array, axis=(0, 1))
            analysis["average_colors"] = avg_colors.tolist()
        
        # Brightness analysis
        if len(img_array.shape) == 3:
            gray = np.mean(img_array, axis=2)
        else:
            gray = img_array
        
        analysis["brightness"] = {
            "mean": float(np.mean(gray)),
            "std": float(np.std(gray)),
            "min": float(np.min(gray)),
            "max": float(np.max(gray))
        }
        
        return analysis
    
    def create_educational_image(self, text: str, subject: str, 
                               size: Tuple[int, int] = (800, 600)) -> Image.Image:
        """Create an educational image with text."""
        # Create blank image
        image = Image.new('RGB', size, color='white')
        draw = ImageDraw.Draw(image)
        
        # Try to load a font
        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()
        
        # Add subject header
        draw.text((20, 20), f"Subject: {subject}", fill='black', font=font)
        
        # Add main text
        draw.text((20, 80), text, fill='black', font=font)
        
        return image

class AudioProcessor:
    """Handles audio processing and analysis."""
    
    def __init__(self):
        self.whisper_model = None
        self._load_models()
    
    def _load_models(self):
        """Load audio processing models."""
        if not WHISPER_AVAILABLE:
            print("⚠️ Whisper not available - audio processing will be limited")
            return
            
        try:
            # Load Whisper model for speech recognition
            self.whisper_model = whisper.load_model("base")
            print("✅ Audio models loaded successfully")
        except Exception as e:
            print(f"⚠️ Warning: Could not load audio models: {e}")
            print("Audio processing will be limited")
    
    def process_audio(self, audio_path: str) -> MultimodalContent:
        """Process an audio file and extract information."""
        if not LIBROSA_AVAILABLE:
            return MultimodalContent(
                content_type="audio",
                content=None,
                metadata={"error": "Librosa not available"},
                source=audio_path,
                timestamp=self._get_timestamp()
            )
            
        try:
            # Load audio
            audio, sr = librosa.load(audio_path)
            
            # Transcribe speech
            transcription = self._transcribe_audio(audio_path)
            
            # Analyze audio characteristics
            analysis = self._analyze_audio_content(audio, sr)
            
            metadata = {
                "transcription": transcription,
                "analysis": analysis,
                "sample_rate": sr,
                "duration": len(audio) / sr
            }
            
            return MultimodalContent(
                content_type="audio",
                content=audio,
                metadata=metadata,
                source=audio_path,
                timestamp=self._get_timestamp()
            )
            
        except Exception as e:
            print(f"❌ Error processing audio {audio_path}: {e}")
            return None
    
    def _transcribe_audio(self, audio_path: str) -> str:
        """Transcribe audio to text using Whisper."""
        if not self.whisper_model:
            return "Audio transcription not available"
        
        try:
            result = self.whisper_model.transcribe(audio_path)
            return result["text"]
        except Exception as e:
            print(f"Error transcribing audio: {e}")
            return "Could not transcribe audio"
    
    def _analyze_audio_content(self, audio: np.ndarray, sr: int) -> Dict[str, Any]:
        """Analyze audio content and characteristics."""
        if not LIBROSA_AVAILABLE:
            return {"error": "Librosa not available"}
            
        analysis = {}
        
        # Basic statistics
        analysis["length"] = len(audio)
        analysis["sample_rate"] = sr
        analysis["duration"] = len(audio) / sr
        
        # Amplitude analysis
        analysis["amplitude"] = {
            "mean": float(np.mean(audio)),
            "std": float(np.std(audio)),
            "min": float(np.min(audio)),
            "max": float(np.max(audio))
        }
        
        # Spectral analysis
        try:
            # Calculate spectrogram
            D = librosa.amplitude_to_db(np.abs(librosa.stft(audio)), ref=np.max)
            analysis["spectral"] = {
                "spectrogram_shape": D.shape,
                "spectral_centroid": float(np.mean(librosa.feature.spectral_centroid(y=audio, sr=sr))),
                "spectral_rolloff": float(np.mean(librosa.feature.spectral_rolloff(y=audio, sr=sr)))
            }
        except Exception as e:
            analysis["spectral"] = {"error": str(e)}
        
        return analysis
    
    def create_audio_summary(self, audio_path: str, max_duration: float = 30.0) -> str:
        """Create a summary of audio content."""
        if not LIBROSA_AVAILABLE:
            return "Audio analysis not available - librosa not installed"
            
        try:
            audio, sr = librosa.load(audio_path)
            duration = len(audio) / sr
            
            if duration <= max_duration:
                return f"Audio duration: {duration:.2f} seconds"
            
            # Analyze key segments
            segments = self._analyze_audio_segments(audio, sr, max_duration)
            
            summary = f"Audio duration: {duration:.2f} seconds\n"
            summary += f"Key segments analyzed: {len(segments)}\n"
            
            for i, segment in enumerate(segments[:3]):  # Top 3 segments
                summary += f"Segment {i+1}: {segment['description']}\n"
            
            return summary
            
        except Exception as e:
            return f"Could not analyze audio: {e}"
    
    def _analyze_audio_segments(self, audio: np.ndarray, sr: int, 
                               segment_duration: float) -> List[Dict[str, Any]]:
        """Analyze audio in segments."""
        segment_length = int(segment_duration * sr)
        segments = []
        
        for i in range(0, len(audio), segment_length):
            segment = audio[i:i + segment_length]
            if len(segment) > 0:
                # Calculate segment energy
                energy = np.mean(segment ** 2)
                
                # Determine if segment has speech (simplified)
                has_speech = energy > np.mean(audio ** 2)
                
                segments.append({
                    "start_time": i / sr,
                    "duration": len(segment) / sr,
                    "energy": float(energy),
                    "has_speech": has_speech,
                    "description": f"High energy segment" if has_speech else "Low energy segment"
                })
        
        return segments

class VideoProcessor:
    """Handles video processing and analysis."""
    
    def __init__(self):
        self.video_processor = None
        self._load_models()
    
    def _load_models(self):
        """Load video processing models."""
        if not MOVIEPY_AVAILABLE:
            print("⚠️ MoviePy not available - video processing will be limited")
            return
            
        try:
            # Load video captioning model
            model_name = "microsoft/git-base-coco"
            self.video_processor = AutoProcessor.from_pretrained(model_name)
            print("✅ Video models loaded successfully")
        except Exception as e:
            print(f"⚠️ Warning: Could not load video models: {e}")
            print("Video processing will be limited")
    
    def process_video(self, video_path: str) -> MultimodalContent:
        """Process a video file and extract information."""
        if not MOVIEPY_AVAILABLE:
            return MultimodalContent(
                content_type="video",
                content=None,
                metadata={"error": "MoviePy not available"},
                source=video_path,
                timestamp=self._get_timestamp()
            )
            
        try:
            # Load video
            video = VideoFileClip(video_path)
            
            # Extract frames for analysis
            frames = self._extract_key_frames(video)
            
            # Extract audio
            audio = video.audio
            audio_analysis = None
            if audio and LIBROSA_AVAILABLE:
                audio_processor = AudioProcessor()
                audio_analysis = audio_processor._analyze_audio_content(
                    np.array(audio.to_soundarray()), audio.fps
                )
            
            # Analyze video content
            analysis = self._analyze_video_content(video, frames)
            
            metadata = {
                "frames_analyzed": len(frames),
                "analysis": analysis,
                "audio_analysis": audio_analysis,
                "duration": video.duration,
                "fps": video.fps,
                "size": video.size
            }
            
            return MultimodalContent(
                content_type="video",
                content=video,
                metadata=metadata,
                source=video_path,
                timestamp=self._get_timestamp()
            )
            
        except Exception as e:
            print(f"❌ Error processing video {video_path}: {e}")
            return None
    
    def _extract_key_frames(self, video, num_frames: int = 10) -> List[np.ndarray]:
        """Extract key frames from video for analysis."""
        if not MOVIEPY_AVAILABLE:
            return []
            
        frames = []
        duration = video.duration
        
        for i in range(num_frames):
            time = (i + 1) * duration / (num_frames + 1)
            frame = video.get_frame(time)
            frames.append(frame)
        
        return frames
    
    def _analyze_video_content(self, video, frames: List[np.ndarray]) -> Dict[str, Any]:
        """Analyze video content and characteristics."""
        analysis = {}
        
        # Basic video info
        analysis["duration"] = video.duration
        analysis["fps"] = video.fps
        analysis["size"] = video.size
        analysis["num_frames"] = len(frames)
        
        # Frame analysis
        if frames:
            frame_analysis = []
            for i, frame in enumerate(frames):
                frame_info = {
                    "frame_index": i,
                    "brightness": float(np.mean(frame)),
                    "contrast": float(np.std(frame))
                }
                frame_analysis.append(frame_info)
            
            analysis["frame_analysis"] = frame_analysis
        
        return analysis
    
    def create_video_summary(self, video_path: str) -> str:
        """Create a summary of video content."""
        if not MOVIEPY_AVAILABLE:
            return "Video analysis not available - moviepy not installed"
            
        try:
            video = VideoFileClip(video_path)
            
            summary = f"Video Summary:\n"
            summary += f"Duration: {video.duration:.2f} seconds\n"
            summary += f"FPS: {video.fps}\n"
            summary += f"Resolution: {video.size[0]}x{video.size[1]}\n"
            
            if video.audio:
                summary += f"Has audio: Yes\n"
                if LIBROSA_AVAILABLE:
                    audio_processor = AudioProcessor()
                    audio_summary = audio_processor.create_audio_summary(video_path)
                    summary += f"Audio: {audio_summary}\n"
                else:
                    summary += f"Audio: Analysis not available\n"
            else:
                summary += f"Has audio: No\n"
            
            return summary
            
        except Exception as e:
            return f"Could not analyze video: {e}"

class MultimodalManager:
    """Manages all multimodal processing capabilities."""
    
    def __init__(self):
        self.image_processor = ImageProcessor()
        self.audio_processor = AudioProcessor()
        self.video_processor = VideoProcessor()
        
        self.supported_formats = {
            "image": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"],
            "audio": [".mp3", ".wav", ".flac", ".m4a", ".aac"],
            "video": [".mp4", ".avi", ".mov", ".mkv", ".wmv"]
        }
    
    def process_file(self, file_path: str) -> Optional[MultimodalContent]:
        """Process any supported file type."""
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext in self.supported_formats["image"]:
            return self.image_processor.process_image(file_path)
        elif file_ext in self.supported_formats["audio"]:
            return self.audio_processor.process_audio(file_path)
        elif file_ext in self.supported_formats["video"]:
            return self.video_processor.process_video(file_path)
        else:
            print(f"❌ Unsupported file format: {file_ext}")
            return None
    
    def create_multimodal_summary(self, file_paths: List[str]) -> str:
        """Create summary of multiple multimodal files."""
        summaries = []
        
        for file_path in file_paths:
            content = self.process_file(file_path)
            if content:
                file_name = Path(file_path).name
                summary = f"\n--- {file_name} ---\n"
                summary += f"Type: {content.content_type}\n"
                
                if content.content_type == "image":
                    summary += f"Caption: {content.metadata.get('caption', 'N/A')}\n"
                    if content.metadata.get('extracted_text'):
                        summary += f"Text: {content.metadata['extracted_text'][:100]}...\n"
                
                elif content.content_type == "audio":
                    summary += f"Transcription: {content.metadata.get('transcription', 'N/A')[:100]}...\n"
                    summary += f"Duration: {content.metadata.get('duration', 0):.2f}s\n"
                
                elif content.content_type == "video":
                    summary += f"Duration: {content.metadata.get('duration', 0):.2f}s\n"
                    summary += f"Resolution: {content.metadata.get('analysis', {}).get('size', 'N/A')}\n"
                
                summaries.append(summary)
        
        return "\n".join(summaries) if summaries else "No files processed"
    
    def generate_educational_content(self, subject: str, content_type: str, 
                                   prompt: str) -> Optional[MultimodalContent]:
        """Generate educational content based on prompts."""
        if content_type == "image":
            # Create educational image
            image = self.image_processor.create_educational_image(prompt, subject)
            
            return MultimodalContent(
                content_type="image",
                content=image,
                metadata={
                    "generated": True,
                    "subject": subject,
                    "prompt": prompt
                },
                source="generated",
                timestamp=self._get_timestamp()
            )
        
        # Add more content generation types here
        return None
    
    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()

class CrossModalAnalyzer:
    """Analyzes relationships between different modalities."""
    
    def __init__(self):
        self.multimodal_manager = MultimodalManager()
    
    def analyze_content_relationships(self, file_paths: List[str]) -> Dict[str, Any]:
        """Analyze relationships between different content types."""
        analysis = {}
        
        # Process all files
        contents = []
        for file_path in file_paths:
            content = self.multimodal_manager.process_file(file_path)
            if content:
                contents.append(content)
        
        if not contents:
            return {"error": "No content processed"}
        
        # Group by content type
        by_type = {}
        for content in contents:
            content_type = content.content_type
            if content_type not in by_type:
                by_type[content_type] = []
            by_type[content_type].append(content)
        
        analysis["content_distribution"] = {
            content_type: len(contents) for content_type, contents in by_type.items()
        }
        
        # Analyze cross-modal relationships
        analysis["cross_modal_insights"] = self._find_cross_modal_insights(contents)
        
        return analysis
    
    def _find_cross_modal_insights(self, contents: List[MultimodalContent]) -> List[str]:
        """Find insights across different modalities."""
        insights = []
        
        # Check for text consistency across modalities
        text_contents = []
        for content in contents:
            if content.content_type == "image" and content.metadata.get("extracted_text"):
                text_contents.append(content.metadata["extracted_text"])
            elif content.content_type == "audio" and content.metadata.get("transcription"):
                text_contents.append(content.metadata["transcription"])
        
        if len(text_contents) > 1:
            # Simple text similarity check
            insights.append(f"Found {len(text_contents)} text sources across different modalities")
        
        # Check for temporal relationships
        video_contents = [c for c in contents if c.content_type == "video"]
        audio_contents = [c for c in contents if c.content_type == "audio"]
        
        if video_contents and audio_contents:
            insights.append("Video and audio content detected - potential for synchronized analysis")
        
        return insights

# Utility functions
def get_supported_formats() -> Dict[str, List[str]]:
    """Get list of supported file formats."""
    return {
        "image": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"],
        "audio": [".mp3", ".wav", ".flac", ".m4a", ".aac"],
        "video": [".mp4", ".avi", ".mov", ".mkv", ".wmv"]
    }

def is_supported_format(file_path: str) -> bool:
    """Check if a file format is supported."""
    file_ext = Path(file_path).suffix.lower()
    all_formats = []
    for formats in get_supported_formats().values():
        all_formats.extend(formats)
    return file_ext in all_formats
