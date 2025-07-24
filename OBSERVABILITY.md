# Observability Setup - Open Source Alternative

This document explains how to use **open-source observability tools** instead of Azure Application Insights for local development.

## 🎯 What's Included

### **Jaeger - Distributed Tracing**
- **Purpose**: Trace requests across microservices
- **UI**: http://localhost:16686
- **Features**: Request flow visualization, performance analysis, error tracking

## 🚀 Quick Start

1. **Start the application**:
   ```bash
   docker-compose up --build
   ```

2. **Access Jaeger UI**:
   - Open http://localhost:16686
   - Select a service from the dropdown
   - Click "Find Traces" to see distributed traces

3. **Access the application**:
   - Frontend: http://localhost:8080
   - Generate some traffic by browsing products

## 📊 Using Jaeger

### **View Traces**
- **Service Map**: See how services communicate
- **Timeline**: Understand request latency 
- **Errors**: Identify failed requests and bottlenecks
- **Dependencies**: Visualize service relationships

### **Key Features**
- ✅ **Zero Configuration**: Works out of the box
- ✅ **Service Discovery**: Automatically detects services
- ✅ **Performance Monitoring**: Track response times
- ✅ **Error Tracking**: Identify failed requests
- ✅ **Dependency Analysis**: Understand service relationships

## 🔧 Configuration

### **Environment Variables**
```bash
# Jaeger endpoints (automatically configured in docker-compose.yml)
JAEGER_ENDPOINT=http://jaeger:14268/api/traces
OTEL_EXPORTER_JAEGER_ENDPOINT=http://jaeger:14268/api/traces
ENABLE_TRACING=1
```

### **Ports**
- **16686**: Jaeger UI
- **14268**: HTTP collector
- **14250**: gRPC collector
- **6831/6832**: UDP agent ports

## 🆚 Comparison with Azure Application Insights

| Feature | Jaeger (Open Source) | Azure Application Insights |
|---------|---------------------|----------------------------|
| **Setup** | Zero config, Docker only | Requires Azure account & setup |
| **Cost** | Free | Pay per GB of telemetry |
| **Tracing** | ✅ Excellent | ✅ Good |
| **Metrics** | Basic | ✅ Advanced |
| **Logs** | Not included | ✅ Full logging |
| **Alerts** | Not included | ✅ Advanced alerting |
| **Local Dev** | ✅ Perfect | Requires cloud connection |

## 🔄 Switching Back to Azure Application Insights

If you want to use Azure Application Insights instead:

1. **Update docker-compose.yml**:
   ```yaml
   environment:
     - APPLICATIONINSIGHTS_CONNECTION_STRING=${APPLICATIONINSIGHTS_CONNECTION_STRING:-}
     - DISABLE_PROFILER=${DISABLE_PROFILER:-}
   ```

2. **Update .env**:
   ```bash
   APPLICATIONINSIGHTS_CONNECTION_STRING="your-connection-string"
   ```

## 🚀 Advanced: Adding Prometheus + Grafana

For complete observability, you can also add:

```yaml
# Add to docker-compose.yml
prometheus:
  image: prom/prometheus:latest
  ports:
    - "9090:9090"

grafana:
  image: grafana/grafana:latest
  ports:
    - "3000:3000"
```

## 🎯 Benefits of This Setup

### **For Development**
- ✅ **No Cloud Dependencies**: Works completely offline
- ✅ **Fast Feedback**: Immediate trace visibility
- ✅ **No Costs**: Free and open source
- ✅ **Easy Debugging**: Visual request flows

### **For Learning**
- ✅ **Industry Standard**: Jaeger is widely adopted
- ✅ **OpenTelemetry Compatible**: Future-proof
- ✅ **Vendor Neutral**: Not locked to any cloud provider

## 🔍 Troubleshooting

### **No Traces Appearing**
1. Check if services are sending traces: `docker-compose logs [service-name]`
2. Verify Jaeger is running: `docker-compose ps jaeger`
3. Check network connectivity: All services should be on `boutique-net`

### **Performance Issues**
- Jaeger stores traces in memory by default
- For production, configure persistent storage

## 📚 Next Steps

1. **Explore Jaeger UI**: Try different search filters
2. **Add Custom Spans**: Instrument your own code
3. **Set up Prometheus**: Add metrics collection
4. **Configure Grafana**: Create custom dashboards

---

**🎉 You now have a complete, open-source observability stack running locally!**

Access Jaeger at: http://localhost:16686
