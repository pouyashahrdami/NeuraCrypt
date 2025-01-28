![NeuraCrypt](banner.jpeg)

# NeuraCrypt

This application bypasses software restrictions that require closing other applications. It operates discreetly, providing an anonymous interface that stays on top of other applications. It is a privacy-focused desktop chat application that integrates with Google's Gemini AI. Running with administrative privileges, the application offers advanced privacy controls, such as window hiding and taskbar concealment.


## 🌟 Features

### Core Functionality

- Direct integration with Google's Gemini AI
- Real-time chat interface
- Message history with scrollable view
- Quick response system with keyboard shortcuts

### Privacy Features

- Runs with administrative privileges
- Hidden from taskbar
- Quick hide/show functionality
- Adjustable opacity
- Generic window title for discretion

### User Interface

- Compact, responsive design
- Customizable window position and size
- Persistent configuration settings
- Status indicators for operations
- Intuitive icon-based controls

## 🚀 Installation

- **YouTube Video for Windows Installation and Configuration API**:  
  [Watch the video here](https://youtu.be/u-Q7Ck4Yotg)

### Prerequisites

- Python 3.8 or higher
- Windows Operating System
- Administrative privileges

### Required Packages

Install the required packages using pip:

```bash
pip install google-generativeai pywin32 keyboard
```

### Configuration

1. Clone or download this repository
2. Run the application once to generate the default `config.json`
3. Edit `config.json` with your API credentials:

```json
{
  "api_key": "YOUR_API_KEY_HERE",
  "model": "gemini-1.5-flash",
  "window": {
    "width": 300,
    "height": 400,
    "x": 1500,
    "y": 100,
    "opacity": 0.4,
  },
  "isadmin": true
}
```

## 🎮 Usage

### Starting the Application

Run the script with Python:

```bash
python main.py
```

The application will automatically request administrative privileges if needed.

### Keyboard Shortcuts

- `F10`: Toggle window visibility
- `Ctrl + Enter`: Send message
- `Enter`: New line in input

### Button Controls

- 📤 Send message
- 🗑️ Clear chat history
- 💥 Close application

### Window Management

- Drag to reposition
- Resize from corners
- Position and size are saved automatically

## ⚙️ Configuration Options

### Window Settings

- `width`: Window width in pixels
- `height`: Window height in pixels
- `x`: Window X position
- `y`: Window Y position
- `opacity`: Window opacity (0.0 to 1.0)

### API Settings

- `api_key`: Your Google Gemini API key
- `model`: Gemini model name

## 🔒 Privacy Considerations

- Application runs with elevated privileges
- Window is hidden from taskbar
- Generic window title
- Quick hide functionality
- Adjustable opacity for discretion

## ⚠️ Security Notes

- Store your API key securely
- Be cautious with administrative privileges
- Monitor application access
- Regularly update dependencies

## 🔧 Troubleshooting

### Common Issues

1. **Permission Denied**

   - Ensure you're running as administrator
   - Check file permissions

2. **API Errors**

   - Verify API key in config.json
   - Check internet connection
   - Confirm API quota availability

3. **Window Not Showing**
   - Use Ctrl+Shift+H to toggle visibility
   - Check task manager for running process
   - Restart application

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests.

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

## 📝 Version History

- 1.0.0: Initial release
  - Basic chat functionality
  - Privacy features
  - Configuration system
  - Window management

- 1.1.0 huge update

*   **New Features:**
    
    *   Added proxy support for enhanced privacy
        
        *   Static proxy configuration
            
        *   Dynamic proxy fetching from external services
            
    *   Tor integration for anonymous communication
        
        *   Tor SOCKS5 proxy support
            
        *   Tor IP renewal functionality
            
    *   Improved error handling for proxy and Tor setup
        
    *   Added dynamic proxy fetching from free proxy services
        
*   **Enhancements:**
    
    *   Better UI responsiveness
        
    *   Improved configuration management
        
    *   Added status indicators for proxy and Tor operations
        
*   **Bug Fixes:**
    
    *   Fixed window resizing issues
        
    *   Resolved proxy connection errors
        
    *   Improved stability during AI responses
## 📞 Support

For support, please:

1. Check the troubleshooting section
2. Review existing issues
3. Create a new issue with detailed information

---

**Note**: This application is intended for legitimate use cases. Please ensure compliance with all applicable laws and regulations in your jurisdiction.
