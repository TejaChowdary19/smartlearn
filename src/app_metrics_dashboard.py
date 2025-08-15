"""
SmartLearn Metrics Dashboard Application
A comprehensive analytics and performance monitoring dashboard
"""

import streamlit as st
import sys
import os

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.metrics_visualization import create_metrics_dashboard, MetricsCollector
from core.advanced_features import SmartLearnAdvanced
import time
import random

# Page configuration
st.set_page_config(
    page_title="SmartLearn Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .status-healthy { color: #28a745; }
    .status-warning { color: #ffc107; }
    .status-critical { color: #dc3545; }
    .dashboard-section {
        background-color: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application function"""
    
    # Header
    st.markdown('<h1 class="main-header">📊 SmartLearn Analytics Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Initialize metrics dashboard
    try:
        dashboard = create_metrics_dashboard()
        metrics_collector = dashboard.metrics_collector
        
        # Sidebar configuration
        with st.sidebar:
            st.header("🎛️ Dashboard Controls")
            
            # Auto-refresh settings
            auto_refresh = st.checkbox("🔄 Auto-refresh", value=True, help="Automatically refresh metrics every 30 seconds")
            refresh_interval = st.slider("Refresh Interval (seconds)", min_value=10, max_value=120, value=30, step=10)
            
            # Data collection settings
            st.subheader("📊 Data Collection")
            enable_collection = st.checkbox("Enable Metrics Collection", value=True)
            
            if enable_collection:
                if not metrics_collector.is_collecting:
                    metrics_collector.start_collection()
                    st.success("✅ Metrics collection started")
                else:
                    st.success("✅ Metrics collection active")
            else:
                if metrics_collector.is_collecting:
                    metrics_collector.stop_collection()
                    st.warning("⚠️ Metrics collection stopped")
                else:
                    st.info("ℹ️ Metrics collection inactive")
            
            # Data export options
            st.subheader("💾 Data Export")
            if st.button("📥 Export Metrics Data"):
                export_metrics_data(metrics_collector)
            
            # System information
            st.subheader("ℹ️ System Info")
            st.info(f"**Platform**: {sys.platform}")
            st.info(f"**Python**: {sys.version.split()[0]}")
            
            # Quick actions
            st.subheader("⚡ Quick Actions")
            if st.button("🧹 Clear Metrics Cache"):
                clear_metrics_cache(metrics_collector)
            
            if st.button("📊 Generate Sample Data"):
                generate_sample_data(metrics_collector)
        
        # Main dashboard content
        if auto_refresh:
            # Auto-refresh logic
            if 'last_refresh' not in st.session_state:
                st.session_state.last_refresh = time.time()
            
            current_time = time.time()
            if current_time - st.session_state.last_refresh >= refresh_interval:
                st.session_state.last_refresh = current_time
                st.rerun()
        
        # Render the main dashboard
        dashboard.render_dashboard()
        
        # Additional custom visualizations
        render_custom_analytics(metrics_collector)
        
        # Performance insights
        render_performance_insights(metrics_collector)
        
    except Exception as e:
        st.error(f"Error initializing dashboard: {e}")
        st.exception(e)

def export_metrics_data(metrics_collector: MetricsCollector):
    """Export metrics data to JSON format"""
    try:
        # Collect all metrics data
        export_data = {
            "export_timestamp": time.time(),
            "performance_metrics": [
                {
                    "timestamp": m.timestamp.isoformat(),
                    "cpu_usage": m.cpu_usage,
                    "memory_usage": m.memory_usage,
                    "gpu_memory_used": m.gpu_memory_used,
                    "gpu_memory_total": m.gpu_memory_total,
                    "response_time": m.response_time,
                    "model_accuracy": m.model_accuracy,
                    "user_engagement": m.user_engagement
                }
                for m in metrics_collector.performance_metrics
            ],
            "training_metrics": [
                {
                    "epoch": m.epoch,
                    "step": m.step,
                    "training_loss": m.training_loss,
                    "validation_loss": m.validation_loss,
                    "learning_rate": m.learning_rate,
                    "accuracy": m.accuracy,
                    "timestamp": m.timestamp.isoformat() if m.timestamp else None
                }
                for m in metrics_collector.training_metrics
            ],
            "user_metrics": [
                {
                    "timestamp": m.timestamp.isoformat(),
                    "user_id": m.user_id,
                    "action": m.action,
                    "subject": m.subject,
                    "difficulty": m.difficulty,
                    "response_time": m.response_time,
                    "accuracy": m.accuracy,
                    "engagement_score": m.engagement_score
                }
                for m in metrics_collector.user_metrics
            ]
        }
        
        # Convert to JSON
        import json
        json_data = json.dumps(export_data, indent=2)
        
        # Create download button
        st.download_button(
            label="📥 Download Metrics Data (JSON)",
            data=json_data,
            file_name=f"smartlearn_metrics_{int(time.time())}.json",
            mime="application/json"
        )
        
        st.success("✅ Metrics data exported successfully!")
        
    except Exception as e:
        st.error(f"Error exporting data: {e}")

def clear_metrics_cache(metrics_collector: MetricsCollector):
    """Clear the metrics cache"""
    try:
        metrics_collector.performance_metrics.clear()
        metrics_collector.training_metrics.clear()
        metrics_collector.user_metrics.clear()
        st.success("✅ Metrics cache cleared successfully!")
        st.rerun()
    except Exception as e:
        st.error(f"Error clearing cache: {e}")

def generate_sample_data(metrics_collector: MetricsCollector):
    """Generate sample metrics data for demonstration"""
    try:
        from datetime import datetime, timedelta
        import random
        
        # Generate sample performance metrics
        base_time = datetime.now() - timedelta(hours=2)
        for i in range(24):
            timestamp = base_time + timedelta(minutes=5*i)
            metrics = metrics_collector.PerformanceMetrics(
                timestamp=timestamp,
                cpu_usage=random.uniform(20, 80),
                memory_usage=random.uniform(40, 90),
                gpu_memory_used=random.uniform(2, 8),
                gpu_memory_total=10.0,
                response_time=random.uniform(100, 3000),
                model_accuracy=random.uniform(0.7, 0.95),
                user_engagement=random.uniform(6, 9)
            )
            metrics_collector.add_performance_metrics(metrics)
        
        # Generate sample training metrics
        for step in range(0, 200, 10):
            metrics = metrics_collector.TrainingMetrics(
                epoch=1,
                step=step,
                training_loss=2.0 * (0.9 ** (step/50)),
                validation_loss=2.2 * (0.9 ** (step/50)),
                learning_rate=1e-4 * (0.95 ** (step/100)),
                accuracy=0.6 + 0.3 * (1 - 0.9 ** (step/50)),
                timestamp=base_time + timedelta(minutes=step)
            )
            metrics_collector.add_training_metrics(metrics)
        
        # Generate sample user metrics
        subjects = ["mathematics", "physics", "computer_science"]
        difficulties = ["beginner", "intermediate", "advanced"]
        actions = ["quiz", "study_plan", "question"]
        
        for i in range(50):
            timestamp = base_time + timedelta(minutes=random.randint(0, 120))
            metrics = metrics_collector.UserMetrics(
                timestamp=timestamp,
                user_id=f"user_{random.randint(1, 10)}",
                action=random.choice(actions),
                subject=random.choice(subjects),
                difficulty=random.choice(difficulties),
                response_time=random.uniform(500, 5000),
                accuracy=random.uniform(0.5, 1.0),
                engagement_score=random.uniform(5, 10)
            )
            metrics_collector.add_user_metrics(metrics)
        
        st.success("✅ Sample data generated successfully!")
        st.rerun()
        
    except Exception as e:
        st.error(f"Error generating sample data: {e}")

def render_custom_analytics(metrics_collector: MetricsCollector):
    """Render additional custom analytics"""
    st.markdown("---")
    st.header("🎯 Custom Analytics & Insights")
    
    # Create columns for custom metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Performance Trends")
        
        # Get recent performance data
        recent_metrics = metrics_collector.get_metrics_history("performance", hours=1)
        
        if recent_metrics:
            # Calculate trends
            cpu_trend = "↗️ Increasing" if len(recent_metrics) > 1 and recent_metrics[-1].cpu_usage > recent_metrics[0].cpu_usage else "↘️ Decreasing"
            memory_trend = "↗️ Increasing" if len(recent_metrics) > 1 and recent_metrics[-1].memory_usage > recent_metrics[0].memory_usage else "↘️ Decreasing"
            
            st.metric("CPU Trend", cpu_trend)
            st.metric("Memory Trend", memory_trend)
            
            # Performance recommendations
            latest = recent_metrics[-1]
            if latest.cpu_usage > 80:
                st.warning("⚠️ High CPU usage detected. Consider optimizing processes.")
            elif latest.cpu_usage < 30:
                st.success("✅ CPU usage is optimal.")
            
            if latest.memory_usage > 80:
                st.warning("⚠️ High memory usage detected. Consider clearing cache.")
            elif latest.memory_usage < 50:
                st.success("✅ Memory usage is optimal.")
        else:
            st.info("Collecting performance data...")
    
    with col2:
        st.subheader("🎓 Learning Analytics")
        
        # Get user metrics
        user_metrics = metrics_collector.get_metrics_history("user", hours=24)
        
        if user_metrics:
            # Calculate learning insights
            total_interactions = len(user_metrics)
            avg_accuracy = sum(m.accuracy for m in user_metrics) / total_interactions
            avg_engagement = sum(m.engagement_score for m in user_metrics) / total_interactions
            
            st.metric("Total Interactions", total_interactions)
            st.metric("Average Accuracy", f"{avg_accuracy:.1%}")
            st.metric("Average Engagement", f"{avg_engagement:.1f}/10")
            
            # Subject popularity
            subject_counts = {}
            for m in user_metrics:
                subject_counts[m.subject] = subject_counts.get(m.subject, 0) + 1
            
            if subject_counts:
                most_popular = max(subject_counts, key=subject_counts.get)
                st.success(f"🎯 Most popular subject: **{most_popular}**")
        else:
            st.info("No user interaction data available.")

def render_performance_insights(metrics_collector: MetricsCollector):
    """Render performance insights and recommendations"""
    st.markdown("---")
    st.header("💡 Performance Insights & Recommendations")
    
    # Get latest metrics
    latest_performance = metrics_collector.get_latest_metrics("performance")
    latest_training = metrics_collector.get_latest_metrics("training")
    
    if latest_performance:
        # Create insights columns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("🖥️ System Health")
            
            # Health score calculation
            health_score = 100
            health_issues = []
            
            if latest_performance.cpu_usage > 80:
                health_score -= 20
                health_issues.append("High CPU usage")
            elif latest_performance.cpu_usage > 60:
                health_score -= 10
                health_issues.append("Moderate CPU usage")
            
            if latest_performance.memory_usage > 80:
                health_score -= 20
                health_issues.append("High memory usage")
            elif latest_performance.memory_usage > 60:
                health_score -= 10
                health_issues.append("Moderate memory usage")
            
            if latest_performance.gpu_memory_used and latest_performance.gpu_memory_total:
                gpu_ratio = latest_performance.gpu_memory_used / latest_performance.gpu_memory_total
                if gpu_ratio > 0.8:
                    health_score -= 20
                    health_issues.append("High GPU memory usage")
                elif gpu_ratio > 0.6:
                    health_score -= 10
                    health_issues.append("Moderate GPU memory usage")
            
            # Display health status
            if health_score >= 80:
                st.success(f"🟢 Excellent Health: {health_score}%")
            elif health_score >= 60:
                st.warning(f"🟡 Good Health: {health_score}%")
            else:
                st.error(f"🔴 Poor Health: {health_score}%")
            
            if health_issues:
                st.write("**Issues detected:**")
                for issue in health_issues:
                    st.write(f"• {issue}")
        
        with col2:
            st.subheader("🚀 Performance Optimization")
            
            # Performance recommendations
            recommendations = []
            
            if latest_performance.cpu_usage > 70:
                recommendations.append("Consider reducing batch size for model inference")
                recommendations.append("Implement request queuing for high load")
            
            if latest_performance.memory_usage > 70:
                recommendations.append("Clear unused model caches")
                recommendations.append("Implement memory-efficient data loading")
            
            if latest_performance.gpu_memory_used and latest_performance.gpu_memory_total:
                gpu_ratio = latest_performance.gpu_memory_used / latest_performance.gpu_memory_total
                if gpu_ratio > 0.7:
                    recommendations.append("Optimize GPU memory allocation")
                    recommendations.append("Consider model quantization")
            
            if recommendations:
                st.write("**Recommendations:**")
                for rec in recommendations:
                    st.write(f"• {rec}")
            else:
                st.success("✅ System is well-optimized!")
        
        with col3:
            st.subheader("📈 Growth Opportunities")
            
            # Identify improvement areas
            opportunities = []
            
            if latest_performance.cpu_usage < 40:
                opportunities.append("CPU resources are underutilized")
                opportunities.append("Consider increasing concurrent users")
            
            if latest_performance.memory_usage < 50:
                opportunities.append("Memory resources are available")
                opportunities.append("Consider caching more data")
            
            if latest_performance.gpu_memory_used and latest_performance.gpu_memory_total:
                gpu_ratio = latest_performance.gpu_memory_used / latest_performance.gpu_memory_total
                if gpu_ratio < 0.5:
                    opportunities.append("GPU memory is underutilized")
                    opportunities.append("Consider larger model batches")
            
            if opportunities:
                st.write("**Opportunities:**")
                for opp in opportunities:
                    st.write(f"• {opp}")
            else:
                st.info("System is well-balanced")
    
    # Training insights
    if latest_training:
        st.subheader("🎓 Training Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Training Progress", f"Step {latest_training.step}")
            st.metric("Current Loss", f"{latest_training.training_loss:.4f}")
            
            if latest_training.validation_loss:
                st.metric("Validation Loss", f"{latest_training.validation_loss:.4f}")
            
            if latest_training.accuracy:
                st.metric("Model Accuracy", f"{latest_training.accuracy:.2%}")
        
        with col2:
            # Training recommendations
            if latest_training.training_loss > 1.0:
                st.warning("⚠️ High training loss. Consider:")
                st.write("• Reducing learning rate")
                st.write("• Increasing training data")
                st.write("• Adjusting model architecture")
            
            if latest_training.validation_loss and latest_training.training_loss:
                if latest_training.validation_loss > latest_training.training_loss * 1.2:
                    st.warning("⚠️ Overfitting detected. Consider:")
                    st.write("• Early stopping")
                    st.write("• Data augmentation")
                    st.write("• Regularization techniques")

if __name__ == "__main__":
    main()
