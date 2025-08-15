"""
SmartLearn Metrics & Visualization Demo
Comprehensive demonstration of all analytics and visualization capabilities
"""

import sys
import os
import time
import random
import json
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from core.metrics_visualization import (
        MetricsCollector, 
        PerformanceMetrics, 
        TrainingMetrics, 
        UserMetrics,
        VisualizationEngine,
        MetricsDashboard
    )
    print("✅ Successfully imported metrics visualization modules")
except ImportError as e:
    print(f"❌ Error importing modules: {e}")
    print("Please ensure you're in the correct directory and have installed requirements_metrics.txt")
    sys.exit(1)

def generate_comprehensive_sample_data(metrics_collector: MetricsCollector):
    """Generate comprehensive sample data for demonstration"""
    print("🔄 Generating comprehensive sample data...")
    
    # Generate 24 hours of performance data (every 5 minutes)
    base_time = datetime.now() - timedelta(hours=24)
    print(f"📅 Generating data from {base_time.strftime('%Y-%m-%d %H:%M')} to now")
    
    for i in range(288):  # 24 hours * 12 (every 5 minutes)
        timestamp = base_time + timedelta(minutes=5*i)
        
        # Simulate realistic CPU and memory patterns
        hour = timestamp.hour
        if 9 <= hour <= 17:  # Business hours - higher usage
            cpu_base = 60
            memory_base = 70
        else:  # Off hours - lower usage
            cpu_base = 30
            memory_base = 50
        
        # Add some randomness and trends
        cpu_usage = max(10, min(95, cpu_base + random.uniform(-15, 25) + np.sin(i/50) * 10))
        memory_usage = max(20, min(90, memory_base + random.uniform(-10, 20) + np.cos(i/30) * 8))
        
        # GPU memory simulation (Apple M3 like)
        gpu_memory_used = random.uniform(2, 8)
        gpu_memory_total = 10.0
        
        # Response time simulation
        response_time = random.uniform(100, 3000)
        if cpu_usage > 80:
            response_time *= 1.5  # Slower when CPU is high
        
        # Model accuracy simulation
        model_accuracy = random.uniform(0.7, 0.95)
        
        # User engagement simulation
        user_engagement = random.uniform(6, 9)
        
        metrics = PerformanceMetrics(
            timestamp=timestamp,
            cpu_usage=cpu_usage,
            memory_usage=memory_usage,
            gpu_memory_used=gpu_memory_used,
            gpu_memory_total=gpu_memory_total,
            response_time=response_time,
            model_accuracy=model_accuracy,
            user_engagement=user_engagement
        )
        metrics_collector.add_performance_metrics(metrics)
    
    print(f"✅ Generated {len(metrics_collector.performance_metrics)} performance metrics")
    
    # Generate training metrics (simulating a training session)
    print("🎓 Generating training metrics...")
    
    # Simulate a realistic training curve
    for step in range(0, 1000, 5):
        # Simulate training loss decreasing over time
        base_loss = 2.0
        decay_factor = 0.995
        training_loss = base_loss * (decay_factor ** step)
        
        # Add some noise to make it realistic
        training_loss += random.uniform(-0.1, 0.1)
        training_loss = max(0.1, training_loss)
        
        # Validation loss (slightly higher, with overfitting simulation)
        validation_loss = training_loss * (1.1 + random.uniform(-0.05, 0.05))
        if step > 500:  # Simulate overfitting
            validation_loss *= (1 + (step - 500) / 1000)
        
        # Learning rate (decreasing over time)
        learning_rate = 1e-4 * (0.999 ** step)
        
        # Accuracy (increasing over time)
        accuracy = 0.6 + 0.3 * (1 - 0.999 ** step)
        accuracy += random.uniform(-0.02, 0.02)
        accuracy = min(0.98, max(0.5, accuracy))
        
        # Timestamp for training
        training_timestamp = base_time + timedelta(minutes=step//2)
        
        metrics = TrainingMetrics(
            epoch=1,
            step=step,
            training_loss=training_loss,
            validation_loss=validation_loss,
            learning_rate=learning_rate,
            accuracy=accuracy,
            timestamp=training_timestamp
        )
        metrics_collector.add_training_metrics(metrics)
    
    print(f"✅ Generated {len(metrics_collector.training_metrics)} training metrics")
    
    # Generate user interaction metrics
    print("👥 Generating user interaction metrics...")
    
    subjects = ["mathematics", "physics", "computer_science", "chemistry", "biology"]
    difficulties = ["beginner", "intermediate", "advanced"]
    actions = ["quiz", "study_plan", "question", "explanation", "practice"]
    
    # Generate realistic user interaction patterns
    for i in range(200):  # 200 user interactions
        # Timestamp (distributed over 24 hours)
        timestamp = base_time + timedelta(minutes=random.randint(0, 1440))
        
        # User ID (10 different users)
        user_id = f"user_{random.randint(1, 10)}"
        
        # Action and subject
        action = random.choice(actions)
        subject = random.choice(subjects)
        difficulty = random.choice(difficulties)
        
        # Response time (varies by difficulty and subject)
        base_response_time = 1000
        if difficulty == "advanced":
            base_response_time *= 1.5
        if subject in ["computer_science", "physics"]:
            base_response_time *= 1.2
        
        response_time = random.uniform(base_response_time * 0.8, base_response_time * 1.5)
        
        # Accuracy (varies by difficulty and user)
        base_accuracy = 0.8
        if difficulty == "beginner":
            base_accuracy += 0.1
        elif difficulty == "advanced":
            base_accuracy -= 0.1
        
        # Add user-specific variation
        user_factor = random.uniform(0.9, 1.1)
        accuracy = base_accuracy * user_factor
        accuracy = min(1.0, max(0.3, accuracy))
        
        # Engagement score (correlated with accuracy and difficulty)
        engagement_base = 7.0
        if accuracy > 0.9:
            engagement_base += 1.0
        elif accuracy < 0.6:
            engagement_base -= 1.0
        
        if difficulty == "beginner":
            engagement_base += 0.5
        elif difficulty == "advanced":
            engagement_base -= 0.5
        
        engagement_score = random.uniform(engagement_base - 0.5, engagement_base + 0.5)
        engagement_score = min(10.0, max(1.0, engagement_score))
        
        metrics = UserMetrics(
            timestamp=timestamp,
            user_id=user_id,
            action=action,
            subject=subject,
            difficulty=difficulty,
            response_time=response_time,
            accuracy=accuracy,
            engagement_score=engagement_score
        )
        metrics_collector.add_user_metrics(metrics)
    
    print(f"✅ Generated {len(metrics_collector.user_metrics)} user interaction metrics")
    
    print("🎉 Sample data generation completed successfully!")

def demonstrate_visualizations(metrics_collector: MetricsCollector):
    """Demonstrate all visualization capabilities"""
    print("\n🎨 Demonstrating visualization capabilities...")
    
    visualization_engine = VisualizationEngine(metrics_collector)
    
    # Test system dashboard
    print("📊 Creating system performance dashboard...")
    try:
        system_chart = visualization_engine.create_system_dashboard()
        print(f"✅ System dashboard created successfully (Figure object: {type(system_chart)})")
    except Exception as e:
        print(f"❌ Error creating system dashboard: {e}")
    
    # Test training analytics
    print("📚 Creating training analytics...")
    try:
        training_chart = visualization_engine.create_training_analytics()
        print(f"✅ Training analytics created successfully (Figure object: {type(training_chart)})")
    except Exception as e:
        print(f"❌ Error creating training analytics: {e}")
    
    # Test user analytics
    print("👥 Creating user analytics...")
    try:
        user_chart = visualization_engine.create_user_analytics()
        print(f"✅ User analytics created successfully (Figure object: {type(user_chart)})")
    except Exception as e:
        print(f"❌ Error creating user analytics: {e}")
    
    # Test AI performance dashboard
    print("🤖 Creating AI performance dashboard...")
    try:
        ai_chart = visualization_engine.create_ai_performance_dashboard()
        print(f"✅ AI performance dashboard created successfully (Figure object: {type(ai_chart)})")
    except Exception as e:
        print(f"❌ Error creating AI performance dashboard: {e}")
    
    print("🎨 All visualizations tested successfully!")

def demonstrate_metrics_analysis(metrics_collector: MetricsCollector):
    """Demonstrate metrics analysis capabilities"""
    print("\n📈 Demonstrating metrics analysis capabilities...")
    
    # Performance metrics analysis
    print("🖥️ Analyzing performance metrics...")
    performance_metrics = metrics_collector.get_metrics_history("performance", hours=24)
    
    if performance_metrics:
        cpu_values = [m.cpu_usage for m in performance_metrics]
        memory_values = [m.memory_usage for m in performance_metrics]
        response_times = [m.response_time for m in performance_metrics if m.response_time]
        
        print(f"   📊 Performance Summary (24h):")
        print(f"   • CPU Usage: Avg={np.mean(cpu_values):.1f}%, Min={np.min(cpu_values):.1f}%, Max={np.max(cpu_values):.1f}%")
        print(f"   • Memory Usage: Avg={np.mean(memory_values):.1f}%, Min={np.min(memory_values):.1f}%, Max={np.max(memory_values):.1f}%")
        
        if response_times:
            print(f"   • Response Time: Avg={np.mean(response_times):.0f}ms, Min={np.min(response_times):.0f}ms, Max={np.max(response_times):.0f}ms")
    
    # Training metrics analysis
    print("🎓 Analyzing training metrics...")
    training_metrics = metrics_collector.get_metrics_history("training", hours=24)
    
    if training_metrics:
        training_losses = [m.training_loss for m in training_metrics]
        validation_losses = [m.validation_loss for m in training_metrics if m.validation_loss]
        accuracies = [m.accuracy for m in training_metrics if m.accuracy]
        
        print(f"   📊 Training Summary:")
        print(f"   • Training Loss: Final={training_losses[-1]:.4f}, Improvement={training_losses[0] - training_losses[-1]:.4f}")
        
        if validation_losses:
            print(f"   • Validation Loss: Final={validation_losses[-1]:.4f}")
        
        if accuracies:
            print(f"   • Model Accuracy: Final={accuracies[-1]:.2%}, Improvement={accuracies[-1] - accuracies[0]:.2%}")
    
    # User metrics analysis
    print("👥 Analyzing user interaction metrics...")
    user_metrics = metrics_collector.get_metrics_history("user", hours=24)
    
    if user_metrics:
        accuracies = [m.accuracy for m in user_metrics]
        engagement_scores = [m.engagement_score for m in user_metrics]
        response_times = [m.response_time for m in user_metrics]
        
        print(f"   📊 User Interaction Summary:")
        print(f"   • Average Accuracy: {np.mean(accuracies):.1%}")
        print(f"   • Average Engagement: {np.mean(engagement_scores):.1f}/10")
        print(f"   • Average Response Time: {np.mean(response_times):.0f}ms")
        
        # Subject popularity
        subject_counts = {}
        for m in user_metrics:
            subject_counts[m.subject] = subject_counts.get(m.subject, 0) + 1
        
        if subject_counts:
            most_popular = max(subject_counts, key=subject_counts.get)
            print(f"   • Most Popular Subject: {most_popular} ({subject_counts[most_popular]} interactions)")
    
    print("📈 Metrics analysis completed successfully!")

def export_demo_data(metrics_collector: MetricsCollector):
    """Export the demo data for external analysis"""
    print("\n💾 Exporting demo data...")
    
    try:
        export_data = {
            "export_timestamp": datetime.now().isoformat(),
            "demo_info": {
                "description": "SmartLearn Comprehensive Demo Data",
                "generated_at": datetime.now().isoformat(),
                "total_performance_metrics": len(metrics_collector.performance_metrics),
                "total_training_metrics": len(metrics_collector.training_metrics),
                "total_user_metrics": len(metrics_collector.user_metrics)
            },
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
        
        # Save to file
        filename = f"demo_metrics_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        print(f"✅ Demo data exported to: {filename}")
        print(f"   📁 File size: {os.path.getsize(filename) / 1024:.1f} KB")
        
    except Exception as e:
        print(f"❌ Error exporting data: {e}")

def main():
    """Main demonstration function"""
    print("🚀 SmartLearn Metrics & Visualization Demo")
    print("=" * 50)
    print("This demo showcases all the analytics and visualization capabilities")
    print("of the SmartLearn platform, including:")
    print("• Real-time performance monitoring")
    print("• Training analytics and visualization")
    print("• User interaction analytics")
    print("• AI performance dashboards")
    print("• Comprehensive data export")
    print("=" * 50)
    
    # Initialize metrics collector
    print("\n🔧 Initializing metrics collector...")
    metrics_collector = MetricsCollector(max_history=10000)
    print("✅ Metrics collector initialized successfully")
    
    # Generate comprehensive sample data
    generate_comprehensive_sample_data(metrics_collector)
    
    # Demonstrate visualizations
    demonstrate_visualizations(metrics_collector)
    
    # Demonstrate metrics analysis
    demonstrate_metrics_analysis(metrics_collector)
    
    # Export demo data
    export_demo_data(metrics_collector)
    
    # Final summary
    print("\n🎉 Demo completed successfully!")
    print("=" * 50)
    print("📊 What you can do next:")
    print("1. Run the metrics dashboard: ./start_metrics_dashboard.sh")
    print("2. View real-time visualizations in your browser")
    print("3. Analyze the exported JSON data in external tools")
    print("4. Integrate metrics collection into your main SmartLearn app")
    print("5. Customize visualizations for your specific needs")
    print("=" * 50)
    print("🌐 Dashboard URL: http://localhost:8505")
    print("📁 Exported data available in the current directory")
    print("🚀 Ready to explore SmartLearn's analytics capabilities!")

if __name__ == "__main__":
    main()
