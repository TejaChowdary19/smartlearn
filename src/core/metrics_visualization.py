"""
SmartLearn Metrics and Visualization System
Provides comprehensive analytics, performance monitoring, and interactive visualizations
"""

import json
import time
import psutil
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import streamlit as st
import altair as alt
from dataclasses import dataclass, asdict
import threading
import queue
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetrics:
    """Data class for storing performance metrics"""
    timestamp: datetime
    cpu_usage: float
    memory_usage: float
    gpu_memory_used: Optional[float] = None
    gpu_memory_total: Optional[float] = None
    response_time: Optional[float] = None
    model_accuracy: Optional[float] = None
    user_engagement: Optional[float] = None

@dataclass
class TrainingMetrics:
    """Data class for storing training metrics"""
    epoch: int
    step: int
    training_loss: float
    learning_rate: float
    validation_loss: Optional[float] = None
    accuracy: Optional[float] = None
    timestamp: datetime = None

@dataclass
class UserMetrics:
    """Data class for storing user interaction metrics"""
    timestamp: datetime
    user_id: str
    action: str
    subject: str
    difficulty: str
    response_time: float
    accuracy: float
    engagement_score: float

class MetricsCollector:
    """Collects and stores real-time metrics"""
    
    def __init__(self, max_history: int = 1000):
        self.max_history = max_history
        self.performance_metrics: List[PerformanceMetrics] = []
        self.training_metrics: List[TrainingMetrics] = []
        self.user_metrics: List[UserMetrics] = []
        self.metrics_queue = queue.Queue()
        self.is_collecting = False
        self.collection_thread = None
        
    def start_collection(self):
        """Start background metrics collection"""
        if not self.is_collecting:
            self.is_collecting = True
            self.collection_thread = threading.Thread(target=self._collect_metrics_loop)
            self.collection_thread.daemon = True
            self.collection_thread.start()
            logger.info("Metrics collection started")
    
    def stop_collection(self):
        """Stop background metrics collection"""
        self.is_collecting = False
        if self.collection_thread:
            self.collection_thread.join(timeout=1)
            logger.info("Metrics collection stopped")
    
    def _collect_metrics_loop(self):
        """Background loop for collecting system metrics"""
        while self.is_collecting:
            try:
                # Collect system metrics
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                
                # Try to get GPU metrics if available
                gpu_memory_used = None
                gpu_memory_total = None
                
                try:
                    import torch
                    if torch.backends.mps.is_available():
                        # Apple M3 GPU metrics
                        gpu_memory_used = torch.mps.current_allocated_memory() / 1024**3  # GB
                        gpu_memory_total = torch.mps.driver_allocated_memory() / 1024**3  # GB
                except ImportError:
                    pass
                
                metrics = PerformanceMetrics(
                    timestamp=datetime.now(),
                    cpu_usage=cpu_percent,
                    memory_usage=memory.percent,
                    gpu_memory_used=gpu_memory_used,
                    gpu_memory_total=gpu_memory_total
                )
                
                self.add_performance_metrics(metrics)
                time.sleep(5)  # Collect every 5 seconds
                
            except Exception as e:
                logger.error(f"Error collecting metrics: {e}")
                time.sleep(10)
    
    def add_performance_metrics(self, metrics: PerformanceMetrics):
        """Add performance metrics to history"""
        self.performance_metrics.append(metrics)
        if len(self.performance_metrics) > self.max_history:
            self.performance_metrics.pop(0)
    
    def add_training_metrics(self, metrics: TrainingMetrics):
        """Add training metrics to history"""
        if metrics.timestamp is None:
            metrics.timestamp = datetime.now()
        self.training_metrics.append(metrics)
        if len(self.training_metrics) > self.max_history:
            self.training_metrics.pop(0)
    
    def add_user_metrics(self, metrics: UserMetrics):
        """Add user interaction metrics to history"""
        self.user_metrics.append(metrics)
        if len(self.user_metrics) > self.max_history:
            self.user_metrics.pop(0)
    
    def get_latest_metrics(self, metric_type: str = "performance") -> Optional[Any]:
        """Get the latest metrics of specified type"""
        if metric_type == "performance" and self.performance_metrics:
            return self.performance_metrics[-1]
        elif metric_type == "training" and self.training_metrics:
            return self.training_metrics[-1]
        elif metric_type == "user" and self.user_metrics:
            return self.user_metrics[-1]
        return None
    
    def get_metrics_history(self, metric_type: str = "performance", 
                          hours: int = 24) -> List[Any]:
        """Get metrics history for specified time period"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        if metric_type == "performance":
            return [m for m in self.performance_metrics if m.timestamp > cutoff_time]
        elif metric_type == "training":
            return [m for m in self.training_metrics if m.timestamp > cutoff_time]
        elif metric_type == "user":
            return [m for m in self.user_metrics if m.timestamp > cutoff_time]
        return []

class VisualizationEngine:
    """Creates interactive visualizations and charts"""
    
    def __init__(self, metrics_collector: MetricsCollector):
        self.metrics_collector = metrics_collector
    
    def create_system_dashboard(self) -> go.Figure:
        """Create comprehensive system performance dashboard"""
        performance_metrics = self.metrics_collector.get_metrics_history("performance", hours=1)
        
        if not performance_metrics:
            # Create empty figure if no data
            fig = go.Figure()
            fig.add_annotation(text="No performance data available", 
                             xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
            return fig
        
        # Prepare data
        timestamps = [m.timestamp for m in performance_metrics]
        cpu_usage = [m.cpu_usage for m in performance_metrics]
        memory_usage = [m.memory_usage for m in performance_metrics]
        gpu_memory_used = [m.gpu_memory_used or 0 for m in performance_metrics]
        
        # Create subplots
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=('CPU Usage (%)', 'Memory Usage (%)', 
                          'GPU Memory Usage (GB)', 'Performance Trends',
                          'Memory Trends', 'Resource Utilization'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # CPU Usage
        fig.add_trace(
            go.Scatter(x=timestamps, y=cpu_usage, mode='lines+markers',
                      name='CPU Usage', line=dict(color='#1f77b4', width=2)),
            row=1, col=1
        )
        
        # Memory Usage
        fig.add_trace(
            go.Scatter(x=timestamps, y=memory_usage, mode='lines+markers',
                      name='Memory Usage', line=dict(color='#ff7f0e', width=2)),
            row=1, col=2
        )
        
        # GPU Memory Usage
        fig.add_trace(
            go.Scatter(x=timestamps, y=gpu_memory_used, mode='lines+markers',
                      name='GPU Memory', line=dict(color='#2ca02c', width=2)),
            row=2, col=1
        )
        
        # Performance Trends
        fig.add_trace(
            go.Scatter(x=timestamps, y=cpu_usage, mode='lines',
                      name='CPU Trend', line=dict(color='#1f77b4')),
            row=2, col=2
        )
        
        # Memory Trends
        fig.add_trace(
            go.Scatter(x=timestamps, y=memory_usage, mode='lines',
                      name='Memory Trend', line=dict(color='#ff7f0e')),
            row=3, col=1
        )
        
        # Resource Utilization Heatmap
        if len(performance_metrics) >= 10:
            # Create time buckets for heatmap
            time_buckets = pd.cut([m.timestamp for m in performance_metrics], 
                                bins=10, labels=False)
            cpu_buckets = pd.cut(cpu_usage, bins=5, labels=False)
            
            heatmap_data = np.zeros((5, 10))
            for i, (t_bucket, c_bucket) in enumerate(zip(time_buckets, cpu_buckets)):
                if not pd.isna(t_bucket) and not pd.isna(c_bucket):
                    heatmap_data[c_bucket][t_bucket] += 1
            
            fig.add_trace(
                go.Heatmap(z=heatmap_data, colorscale='Viridis',
                          name='Resource Heatmap'),
                row=3, col=2
            )
        
        # Update layout
        fig.update_layout(
            height=800,
            title_text="SmartLearn System Performance Dashboard",
            showlegend=True,
            template="plotly_white"
        )
        
        return fig
    
    def create_training_analytics(self) -> go.Figure:
        """Create training metrics visualization"""
        training_metrics = self.metrics_collector.get_metrics_history("training", hours=24)
        
        if not training_metrics:
            fig = go.Figure()
            fig.add_annotation(text="No training data available", 
                             xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
            return fig
        
        # Prepare data
        steps = [m.step for m in training_metrics]
        training_loss = [m.training_loss for m in training_metrics]
        validation_loss = [m.validation_loss for m in training_metrics if m.validation_loss]
        accuracy = [m.accuracy for m in training_metrics if m.accuracy]
        learning_rate = [m.learning_rate for m in training_metrics]
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Training Loss', 'Validation Loss', 
                          'Model Accuracy', 'Learning Rate'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Training Loss
        fig.add_trace(
            go.Scatter(x=steps, y=training_loss, mode='lines+markers',
                      name='Training Loss', line=dict(color='#d62728', width=2)),
            row=1, col=1
        )
        
        # Validation Loss
        if validation_loss:
            fig.add_trace(
                go.Scatter(x=steps[:len(validation_loss)], y=validation_loss, 
                          mode='lines+markers', name='Validation Loss',
                          line=dict(color='#9467bd', width=2)),
                row=1, col=2
            )
        
        # Model Accuracy
        if accuracy:
            fig.add_trace(
                go.Scatter(x=steps[:len(accuracy)], y=accuracy, mode='lines+markers',
                          name='Accuracy', line=dict(color='#2ca02c', width=2)),
                row=2, col=1
            )
        
        # Learning Rate
        fig.add_trace(
            go.Scatter(x=steps, y=learning_rate, mode='lines+markers',
                      name='Learning Rate', line=dict(color='#ff7f0e', width=2)),
            row=2, col=2
        )
        
        # Update layout
        fig.update_layout(
            height=600,
            title_text="SmartLearn Training Analytics",
            showlegend=True,
            template="plotly_white"
        )
        
        return fig
    
    def create_user_analytics(self) -> go.Figure:
        """Create user interaction analytics visualization"""
        user_metrics = self.metrics_collector.get_metrics_history("user", hours=24)
        
        if not user_metrics:
            fig = go.Figure()
            fig.add_annotation(text="No user data available", 
                             xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
            return fig
        
        # Prepare data for analysis
        df = pd.DataFrame([asdict(m) for m in user_metrics])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('User Engagement Over Time', 'Subject Performance', 
                          'Response Time Analysis', 'Difficulty Distribution'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # User Engagement Over Time
        engagement_by_hour = df.groupby(df['timestamp'].dt.hour)['engagement_score'].mean()
        fig.add_trace(
            go.Bar(x=engagement_by_hour.index, y=engagement_by_hour.values,
                   name='Avg Engagement', marker_color='#1f77b4'),
            row=1, col=1
        )
        
        # Subject Performance
        subject_performance = df.groupby('subject')['accuracy'].mean().sort_values(ascending=True)
        fig.add_trace(
            go.Bar(x=subject_performance.values, y=subject_performance.index,
                   orientation='h', name='Subject Performance',
                   marker_color='#ff7f0e'),
            row=1, col=2
        )
        
        # Response Time Analysis
        response_time_by_subject = df.groupby('subject')['response_time'].mean()
        fig.add_trace(
            go.Bar(x=response_time_by_subject.index, y=response_time_by_subject.values,
                   name='Avg Response Time', marker_color='#2ca02c'),
            row=2, col=1
        )
        
        # Difficulty Distribution
        difficulty_counts = df['difficulty'].value_counts()
        fig.add_trace(
            go.Bar(x=difficulty_counts.index, y=difficulty_counts.values,
                   name='Difficulty Distribution', marker_color='#9467bd'),
            row=2, col=2
        )
        
        # Update layout
        fig.update_layout(
            height=600,
            title_text="SmartLearn User Analytics",
            showlegend=True,
            template="plotly_white"
        )
        
        return fig
    
    def create_ai_performance_dashboard(self) -> go.Figure:
        """Create AI model performance dashboard"""
        # Get latest metrics
        latest_performance = self.metrics_collector.get_latest_metrics("performance")
        latest_training = self.metrics_collector.get_latest_metrics("training")
        
        # Create comprehensive AI dashboard
        fig = make_subplots(
            rows=2, cols=3,
            subplot_titles=('Response Time', 'Memory Usage', 'GPU Usage',
                          'Training Progress', 'Model Accuracy', 'System Health'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Model Response Time
        response_time = latest_performance.response_time if latest_performance else 0
        fig.add_trace(
            go.Bar(x=['Response Time'], y=[response_time],
                   name='Response Time (ms)', marker_color='darkgreen'),
            row=1, col=1
        )
        
        # Memory Usage
        memory_usage = latest_performance.memory_usage if latest_performance else 0
        fig.add_trace(
            go.Bar(x=['Memory Usage'], y=[memory_usage],
                   name='Memory Usage (%)', marker_color='darkblue'),
            row=1, col=2
        )
        
        # GPU Usage
        gpu_usage = 0
        if latest_performance and latest_performance.gpu_memory_used and latest_performance.gpu_memory_total:
            gpu_usage = (latest_performance.gpu_memory_used / latest_performance.gpu_memory_total) * 100
        
        fig.add_trace(
            go.Bar(x=['GPU Usage'], y=[gpu_usage],
                   name='GPU Usage (%)', marker_color='darkred'),
            row=1, col=3
        )
        
        # Training Progress
        if latest_training:
            progress_percentage = (latest_training.step / 1000) * 100  # Assuming 1000 steps total
            fig.add_trace(
                go.Bar(x=['Training Progress'], y=[progress_percentage],
                       name='Training Progress (%)', marker_color='purple'),
                row=2, col=1
            )
        
        # Model Accuracy
        accuracy = latest_training.accuracy if latest_training else 0
        fig.add_trace(
            go.Bar(x=['Model Accuracy'], y=[accuracy * 100 if accuracy else 0],
                   name='Model Accuracy (%)', marker_color='darkgreen'),
            row=2, col=2
        )
        
        # System Health Score
        health_score = 100
        if latest_performance:
            if latest_performance.cpu_usage > 80:
                health_score -= 20
            if latest_performance.memory_usage > 80:
                health_score -= 20
            if latest_performance.gpu_memory_used and latest_performance.gpu_memory_total:
                gpu_ratio = latest_performance.gpu_memory_used / latest_performance.gpu_memory_total
                if gpu_ratio > 0.8:
                    health_score -= 20
        
        fig.add_trace(
            go.Bar(x=['System Health'], y=[health_score],
                   name='System Health (%)', marker_color='darkgreen'),
            row=2, col=3
        )
        
        # Update layout
        fig.update_layout(
            height=700,
            title_text="SmartLearn AI Performance Dashboard",
            showlegend=False,
            template="plotly_white"
        )
        
        return fig

class MetricsDashboard:
    """Main dashboard class for displaying all metrics and visualizations"""
    
    def __init__(self, metrics_collector: MetricsCollector):
        self.metrics_collector = metrics_collector
        self.visualization_engine = VisualizationEngine(metrics_collector)
    
    def render_dashboard(self):
        """Render the complete metrics dashboard"""
        st.title("📊 SmartLearn Analytics & Performance Dashboard")
        st.markdown("---")
        
        # Start metrics collection if not already running
        if not self.metrics_collector.is_collecting:
            self.metrics_collector.start_collection()
        
        # Create tabs for different dashboard sections
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🏠 System Overview", 
            "🤖 AI Performance", 
            "📚 Training Analytics",
            "👥 User Analytics",
            "📈 Real-time Metrics"
        ])
        
        with tab1:
            self._render_system_overview()
        
        with tab2:
            self._render_ai_performance()
        
        with tab3:
            self._render_training_analytics()
        
        with tab4:
            self._render_user_analytics()
        
        with tab5:
            self._render_realtime_metrics()
    
    def _render_system_overview(self):
        """Render system overview dashboard"""
        st.header("🖥️ System Performance Overview")
        
        # Get latest metrics
        latest_metrics = self.metrics_collector.get_latest_metrics("performance")
        
        if latest_metrics:
            # Create metric cards
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    label="CPU Usage",
                    value=f"{latest_metrics.cpu_usage:.1f}%",
                    delta=f"{latest_metrics.cpu_usage - 50:.1f}%" if latest_metrics.cpu_usage > 50 else None
                )
            
            with col2:
                st.metric(
                    label="Memory Usage",
                    value=f"{latest_metrics.memory_usage:.1f}%",
                    delta=f"{latest_metrics.memory_usage - 70:.1f}%" if latest_metrics.memory_usage > 70 else None
                )
            
            with col3:
                if latest_metrics.gpu_memory_used:
                    gpu_usage = (latest_metrics.gpu_memory_used / latest_metrics.gpu_memory_total) * 100
                    st.metric(
                        label="GPU Usage",
                        value=f"{gpu_usage:.1f}%",
                        delta=f"{gpu_usage - 60:.1f}%" if gpu_usage > 60 else None
                    )
                else:
                    st.metric(label="GPU Usage", value="N/A")
            
            with col4:
                st.metric(
                    label="System Health",
                    value="🟢 Healthy" if latest_metrics.cpu_usage < 80 and latest_metrics.memory_usage < 80 else "🟡 Warning" if latest_metrics.cpu_usage < 90 and latest_metrics.memory_usage < 90 else "🔴 Critical"
                )
            
            # System performance chart
            st.subheader("📈 System Performance Trends")
            system_chart = self.visualization_engine.create_system_dashboard()
            st.plotly_chart(system_chart, use_container_width=True)
            
        else:
            st.info("Collecting system metrics... Please wait a moment.")
            st.progress(0)
            time.sleep(2)
            st.rerun()
    
    def _render_ai_performance(self):
        """Render AI performance dashboard"""
        st.header("🤖 AI Model Performance")
        
        # AI Performance dashboard
        ai_chart = self.visualization_engine.create_ai_performance_dashboard()
        st.plotly_chart(ai_chart, use_container_width=True)
        
        # Performance insights
        st.subheader("💡 Performance Insights")
        
        latest_performance = self.metrics_collector.get_latest_metrics("performance")
        if latest_performance:
            col1, col2 = st.columns(2)
            
            with col1:
                st.info(f"**Current Response Time**: {latest_performance.response_time or 'N/A'} ms")
                st.info(f"**Memory Efficiency**: {latest_performance.memory_usage:.1f}%")
                
            with col2:
                if latest_performance.gpu_memory_used:
                    gpu_efficiency = (latest_performance.gpu_memory_used / latest_performance.gpu_memory_total) * 100
                    st.success(f"**GPU Memory Efficiency**: {gpu_efficiency:.1f}%")
                else:
                    st.warning("**GPU Metrics**: Not available")
    
    def _render_training_analytics(self):
        """Render training analytics dashboard"""
        st.header("📚 Model Training Analytics")
        
        # Training analytics chart
        training_chart = self.visualization_engine.create_training_analytics()
        st.plotly_chart(training_chart, use_container_width=True)
        
        # Training insights
        st.subheader("🎯 Training Insights")
        
        training_metrics = self.metrics_collector.get_metrics_history("training", hours=24)
        if training_metrics:
            latest_training = training_metrics[-1]
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    label="Current Loss",
                    value=f"{latest_training.training_loss:.4f}",
                    delta=f"{latest_training.training_loss - training_metrics[0].training_loss:.4f}" if len(training_metrics) > 1 else None
                )
            
            with col2:
                if latest_training.validation_loss:
                    st.metric(
                        label="Validation Loss",
                        value=f"{latest_training.validation_loss:.4f}"
                    )
                else:
                    st.metric(label="Validation Loss", value="N/A")
            
            with col3:
                if latest_training.accuracy:
                    st.metric(
                        label="Model Accuracy",
                        value=f"{latest_training.accuracy:.2%}"
                    )
                else:
                    st.metric(label="Model Accuracy", value="N/A")
        else:
            st.info("No training data available. Start training to see analytics.")
    
    def _render_user_analytics(self):
        """Render user analytics dashboard"""
        st.header("👥 User Interaction Analytics")
        
        # User analytics chart
        user_chart = self.visualization_engine.create_user_analytics()
        st.plotly_chart(user_chart, use_container_width=True)
        
        # User insights
        st.subheader("📊 User Engagement Insights")
        
        user_metrics = self.metrics_collector.get_metrics_history("user", hours=24)
        if user_metrics:
            df = pd.DataFrame([asdict(m) for m in user_metrics])
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                avg_engagement = df['engagement_score'].mean()
                st.metric(
                    label="Average Engagement",
                    value=f"{avg_engagement:.2f}/10"
                )
            
            with col2:
                avg_accuracy = df['accuracy'].mean()
                st.metric(
                    label="Average Accuracy",
                    value=f"{avg_accuracy:.1%}"
                )
            
            with col3:
                avg_response_time = df['response_time'].mean()
                st.metric(
                    label="Average Response Time",
                    value=f"{avg_response_time:.0f} ms"
                )
            
            # Subject performance table
            st.subheader("📚 Subject Performance Summary")
            subject_summary = df.groupby('subject').agg({
                'accuracy': ['mean', 'count'],
                'engagement_score': 'mean',
                'response_time': 'mean'
            }).round(3)
            
            st.dataframe(subject_summary, use_container_width=True)
        else:
            st.info("No user interaction data available. User interactions will appear here.")
    
    def _render_realtime_metrics(self):
        """Render real-time metrics"""
        st.header("📈 Real-time Performance Monitoring")
        
        # Auto-refresh every 5 seconds
        if st.button("🔄 Refresh Metrics", key="refresh_metrics"):
            st.rerun()
        
        # Real-time metrics display
        placeholder = st.empty()
        
        with placeholder.container():
            latest_metrics = self.metrics_collector.get_latest_metrics("performance")
            
            if latest_metrics:
                # Create real-time charts
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("🖥️ CPU & Memory Usage")
                    
                    # Get recent data for real-time chart
                    recent_metrics = self.metrics_collector.get_metrics_history("performance", hours=1)
                    if len(recent_metrics) > 1:
                        timestamps = [m.timestamp.strftime('%H:%M:%S') for m in recent_metrics]
                        cpu_values = [m.cpu_usage for m in recent_metrics]
                        memory_values = [m.memory_usage for m in recent_metrics]
                        
                        chart_data = pd.DataFrame({
                            'Time': timestamps,
                            'CPU (%)': cpu_values,
                            'Memory (%)': memory_values
                        })
                        
                        chart = alt.Chart(chart_data).mark_line().encode(
                            x='Time',
                            y='value',
                            color='variable'
                        ).transform_fold(
                            ['CPU (%)', 'Memory (%)'],
                            as_=['variable', 'value']
                        )
                        
                        st.altair_chart(chart, use_container_width=True)
                
                with col2:
                    st.subheader("📊 System Status")
                    
                    # Status indicators
                    cpu_status = "🟢" if latest_metrics.cpu_usage < 70 else "🟡" if latest_metrics.cpu_usage < 90 else "🔴"
                    memory_status = "🟢" if latest_metrics.memory_usage < 70 else "🟡" if latest_metrics.memory_usage < 90 else "🔴"
                    
                    st.markdown(f"""
                    - **CPU**: {cpu_status} {latest_metrics.cpu_usage:.1f}%
                    - **Memory**: {memory_status} {latest_metrics.memory_usage:.1f}%
                    """)
                    
                    if latest_metrics.gpu_memory_used:
                        gpu_usage = (latest_metrics.gpu_memory_used / latest_metrics.gpu_memory_total) * 100
                        gpu_status = "🟢" if gpu_usage < 70 else "🟡" if gpu_usage < 90 else "🔴"
                        st.markdown(f"- **GPU**: {gpu_status} {gpu_usage:.1f}%")
                    
                    # System recommendations
                    st.subheader("💡 Recommendations")
                    if latest_metrics.cpu_usage > 80:
                        st.warning("High CPU usage detected. Consider optimizing model inference.")
                    if latest_metrics.memory_usage > 80:
                        st.warning("High memory usage detected. Consider clearing cache.")
                    if latest_metrics.cpu_usage < 30 and latest_metrics.memory_usage < 50:
                        st.success("System running optimally!")
            
            else:
                st.info("Collecting real-time metrics...")
                st.progress(0)
                time.sleep(1)
                st.rerun()

# Utility functions for easy integration
def create_metrics_dashboard() -> MetricsDashboard:
    """Create and return a metrics dashboard instance"""
    metrics_collector = MetricsCollector()
    return MetricsDashboard(metrics_collector)

def add_training_metrics(epoch: int, step: int, training_loss: float, 
                        validation_loss: Optional[float] = None, 
                        learning_rate: float = 1e-4, accuracy: Optional[float] = None):
    """Utility function to add training metrics"""
    global _global_metrics_collector
    
    if '_global_metrics_collector' not in globals():
        _global_metrics_collector = MetricsCollector()
    
    metrics = TrainingMetrics(
        epoch=epoch,
        step=step,
        training_loss=training_loss,
        validation_loss=validation_loss,
        learning_rate=learning_rate,
        accuracy=accuracy
    )
    
    _global_metrics_collector.add_training_metrics(metrics)

def add_user_interaction(user_id: str, action: str, subject: str, difficulty: str,
                        response_time: float, accuracy: float, engagement_score: float):
    """Utility function to add user interaction metrics"""
    global _global_metrics_collector
    
    if '_global_metrics_collector' not in globals():
        _global_metrics_collector = MetricsCollector()
    
    metrics = UserMetrics(
        timestamp=datetime.now(),
        user_id=user_id,
        action=action,
        subject=subject,
        difficulty=difficulty,
        response_time=response_time,
        accuracy=accuracy,
        engagement_score=engagement_score
    )
    
    _global_metrics_collector.add_user_metrics(metrics)

def get_metrics_collector() -> MetricsCollector:
    """Get the global metrics collector instance"""
    global _global_metrics_collector
    
    if '_global_metrics_collector' not in globals():
        _global_metrics_collector = MetricsCollector()
    
    return _global_metrics_collector
