# Technical Specification: Automated Online Course Video Generation System

**Project Name:** AI Video Course Generator  
**Version:** 1.0  
**Date:** March 27, 2026  
**Author:** Technical Architecture Team  
**Target Market:** USA

-----

## Executive Summary

This document describes a fully automated system for generating online course videos with lip-synced presenters, infographics, diagrams, and b-roll footage. The system accepts text scripts, presenter photos, and course parameters as input, then outputs production-ready video segments via API-driven workflows—no manual editing required.

**Core Requirements:**

  * API-first architecture: all operations programmatically controllable
  * Automated lip-sync video generation from text/audio scripts
  * Dynamic infographic and diagram generation
  * Automated b-roll and scene generation
  * Automatic video assembly and delivery
  * Scalable, cloud-native infrastructure
  * Available in US market

-----

## System Architecture Overview

### High-Level Component Diagram

**Figure 1: System Architecture Diagram**

**Components:**

  * **API Gateway & Orchestrator** - receives course generation requests, manages workflow state, coordinates service calls
  * **Content Processing Engine** - parses scripts, segments lessons, extracts metadata, generates prompts
  * **Avatar Video Generator** - creates lip-synced talking head segments (HeyGen API)
  * **Infographic Generator** - produces charts, diagrams, branded graphics (ContentDrips API)
  * **Scene & B-Roll Generator** - generates supplementary video clips (WaveSpeedAI API)
  * **Video Assembly Service** - stitches segments, adds transitions, outputs final videos (FFmpeg)
  * **Storage & Delivery** - manages assets, serves videos via CDN (AWS S3 + CloudFront)
  * **Job Queue & Monitoring** - handles async processing, retry logic, status tracking

-----

## Technology Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **API Gateway** | Node.js/Express or FastAPI (Python) | Request routing, authentication, rate limiting |
| **Orchestration** | Temporal.io or AWS Step Functions | Workflow management, state persistence |
| **Job Queue** | Redis + BullMQ or AWS SQS | Async task processing, retries |
| **Storage** | AWS S3 | Video assets, scripts, metadata |
| **CDN** | AWS CloudFront | Fast video delivery globally |
| **Video Processing** | FFmpeg | Concatenation, transcoding, overlays |
| **Monitoring** | Datadog or Prometheus + Grafana | Performance metrics, error tracking |
| **Database** | PostgreSQL | Course metadata, job status, user data |

-----

## Service Selection & API Integration

### 1\. HeyGen - Talking Head / Lip-Sync Avatar Generation

**Role:** Primary service for generating presenter videos with accurate lip-sync.

**Key Features:**

  * Custom avatar creation from user photos
  * Text-to-speech with lip-sync synchronization
  * Multi-language support (175+ languages)
  * API-first design with RESTful endpoints
  * Enterprise-grade reliability

**API Endpoints:**

| Endpoint | Purpose |
| :--- | :--- |
| `POST /v2/photo_avatar` | Create custom avatar from photo |
| `POST /v2/video/generate` | Generate lip-synced video from script |
| `GET /v1/video.status` | Check generation status |
| `GET /v2/avatars` | List available avatars |
| `POST /v2/voices` | List compatible voices |

**Table 1: HeyGen API Core Endpoints**

**Pricing (March 2026):**

  * **API Pro Plan:** $99/month, $0.99 per credit, 100 credits included
  * **API Scale Plan:** $330/month, $0.50 per credit, 660 credits included
  * **Pay-as-you-go:** Starting at $5, no monthly commitment
  * **Typical talking head video (1 min):** \~10-15 credits

**Rate Limits:**

  * Free tier: 3 videos/month, 720p, watermarked
  * Pro: Up to 15 concurrent generations
  * Scale: Up to 30 concurrent generations
  * Enterprise: Custom concurrency + SLAs

**Implementation Example:**

```javascript
// Create custom avatar (one-time setup)
const avatarResponse = await fetch('https://api.heygen.com/v2/photo_avatar', {
  method: 'POST',
  headers: {
    'X-Api-Key': process.env.HEYGEN_API_KEY,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    avatar_name: 'Course Presenter',
    photos: ['https://yourstorage.com/presenter.jpg']
  })
});
const { avatar_id } = await avatarResponse.json();

// Generate video segment
const videoResponse = await fetch('https://api.heygen.com/v2/video/generate', {
  method: 'POST',
  headers: {
    'X-Api-Key': process.env.HEYGEN_API_KEY,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    video_inputs: [{
      character: {
        type: 'avatar',
        avatar_id: avatar_id,
        avatar_style: 'normal'
      },
      voice: {
        type: 'text',
        input_text: 'Welcome to lesson 1. Today we will explore...',
        voice_id: 'en-US-JennyNeural'
      }
    }],
    dimension: { width: 1920, height: 1080 },
    aspect_ratio: '16:9'
  })
});
const { video_id } = await videoResponse.json();

// Poll for completion
const checkStatus = async (videoId) => {
  const statusRes = await fetch(
    `https://api.heygen.com/v1/video.status?video_id=${videoId}`,
    { headers: { 'X-Api-Key': process.env.HEYGEN_API_KEY } }
  );
  const { data } = await statusRes.json();
  return data; // status: 'completed', video_url: 'https://...'
};
```

### 2\. WaveSpeedAI – B-Roll, Scenes, and Visual Enhancements

**Role:** Unified API gateway to multiple video generation models for supplementary content.

**Available Models (March 2026):**

| Model | Price/sec | Best For | Max Duration |
| :--- | :--- | :--- | :--- |
| **Kling 2.0** | Variable | Long clips, lectures | 120 sec |
| **Seedance** | $0.04/img | Image animation, portraits | N/A |
| **Sora 2** | $0.10 | Cinematic quality | 60 sec |
| **Wan 2.2 Ultra Fast** | $0.01 | Quick iterations, social | 30 sec |
| **InfiniteTalk** | $0.03 | Portrait animation | Variable |
| **Veo 3.1** | $0.40 | Premium commercial | 30 sec |

**Table 2: WaveSpeedAI Model Pricing**

**API Endpoints:**

```javascript
// Generate b-roll scene
const sceneResponse = await fetch('https://api.wavespeed.ai/v1/generate/video', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${process.env.WAVESPEED_API_KEY}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    model: 'kling-2.0',
    prompt: 'Modern office workspace with computers and natural lighting, professional, 4K',
    duration: 10,
    aspect_ratio: '16:9',
    quality: 'high'
  })
});
const { job_id } = await sceneResponse.json();

// Check generation status
const statusResponse = await fetch(
  `https://api.wavespeed.ai/v1/jobs/${job_id}`,
  { headers: { 'Authorization': `Bearer ${process.env.WAVESPEED_API_KEY}` } }
);
const { status, video_url } = await statusResponse.json();
```

**Recommended Model Selection by Use Case:**

  * Long lecture segments (30-120 sec): Kling 2.0 - temporal consistency
  * Quick product demos: Wan 2.2 Ultra Fast - cost-effective, fast
  * Animate diagrams/charts: Seedance (image-to-video) – preserves details
  * Premium cinematic intros: Sora 2 or Veo 3.1 - highest quality
  * Talking portraits (if needed): InfiniteTalk - lip-sync capable

**Pricing Structure:**

  * Pay-per-use, no monthly minimums
  * $1 free credits on signup
  * Volume discounts available for \>$1000/month spend
  * Enterprise plans: dedicated support, SLAs, priority processing

### 3\. ContentDrips - Infographic and Diagram Generation

**Role:** API-driven branded infographic and carousel generation.

**Key Features:**

  * REST API with single-call generation
  * Auto-branding: pass logo, colors, fonts once
  * Multi-slide carousel support (intro, content, ending)
  * Export formats: PNG, PDF
  * Async job processing with webhooks

**API Endpoints:**

```javascript
// Generate branded infographic
const infographicResponse = await fetch(
  'https://generate.contentdrips.com/render?tool=carousel-maker',
  {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${process.env.CONTENTDRIPS_API_KEY}`
    },
    body: JSON.stringify({
      template_id: 'educational-stats-template',
      output: 'png',
      branding: {
        name: 'YourCourse Academy',
        logo_url: 'https://yourstorage.com/logo.png',
        primary_color: '#1E88E5',
        secondary_color: '#FFC107'
      },
      carousel: {
        intro_slide: {
          heading: 'Key Statistics',
          description: '2024 Market Overview'
        },
        slides: [
          { heading: '95% Growth', description: 'Year-over-year increase' },
          { heading: '$2.4B Market', description: 'Total addressable market' },
          { heading: '120 Countries', description: 'Global reach' }
        ],
        ending_slide: {
          heading: 'Learn More',
          description: 'Visit our course for details'
        }
      }
    })
  }
);
const { job_id } = await infographicResponse.json();

// Poll for result
const resultResponse = await fetch(
  `https://generate.contentdrips.com/job/${job_id}/result`
);
const { export_url } = await resultResponse.json();
// export_url: direct link to PNG/PDF
```

**Pricing (March 2026):**

  * Free: $0, 50 one-time credits (testing only)
  * Basic API: $39/month, moderate usage
  * Advanced API: $149/month, high-volume
  * Pro API: $359/month, commercial scale + priority support

**Rate Limits:**

  * Basic: \~500 generations/month
  * Advanced: \~2000 generations/month
  * Pro: \~5000 generations/month
  * Custom enterprise: unlimited with SLA

**Alternative Option: Infogram**
If you need interactive charts/graphs (not static images), consider Infogram:

  * Programmatic chart generation
  * Data-driven visualizations (bar, line, pie, maps)
  * Export as PNG/SVG/interactive embed
  * API available on business plans (contact sales)

### 4\. FFmpeg - Video Assembly and Post-Processing

**Role:** Stitch video segments, add transitions, normalize audio, transcode formats.

**Why FFmpeg:**

  * Open-source, battle-tested, production-grade
  * Handles all video formats and codecs
  * Programmable via command-line or bindings (fluent-ffmpeg for Node.js, ffmpeg-python)
  * Runs on Linux servers, containers, serverless (with Lambda layers)

**Common Operations:**

| Operation | FFmpeg Command Example |
| :--- | :--- |
| Concatenate videos | `ffmpeg -f concat -i list.txt -c copy out.mp4` |
| Add fade transition | `-vf "fade=in:0:30,fade=out:270:30"` |
| Overlay image | `-i logo.png -filter_complex overlay=x:y` |
| Normalize audio | `-af loudnorm` |
| Transcode to H.264 | `-c:v libx264 -crf 23 -preset medium` |

**Table 3: Common FFmpeg Operations**

**Concatenation Workflow Example:**

```javascript
// Using fluent-ffmpeg (Node.js)
const ffmpeg = require('fluent-ffmpeg');
const fs = require('fs');

// Create concat file list
const segments = [
  { file: 'intro_avatar.mp4', duration: 15 },
  { file: 'infographic_01.mp4', duration: 8 },
  { file: 'lecture_avatar.mp4', duration: 120 },
  { file: 'broll_scene.mp4', duration: 10 },
  { file: 'outro_avatar.mp4', duration: 12 }
];
const concatList = segments.map(s => `file '${s.file}'`).join('\n');
fs.writeFileSync('/tmp/concat.txt', concatList);

// Concatenate
ffmpeg()
  .input('/tmp/concat.txt')
  .inputOptions(['-f concat', '-safe 0'])
  .outputOptions(['-c copy']) // fast, no re-encode
  .output('/tmp/final_lesson.mp4')
  .on('end', () => console.log('Video assembly complete'))
  .on('error', (err) => console.error('FFmpeg error:', err))
  .run();
```

**Best Practices:**

  * Ensure all segments have same resolution, frame rate, codec for -c copy (fast)
  * If resolutions differ, re-encode with scaling: `-vf scale=1920:1080`
  * Add fade transitions between segments for professional look
  * Normalize audio levels across segments to avoid volume jumps
  * Use hardware acceleration if available (-hwaccel cuda on GPU instances)

### 5\. AWS S3 + CloudFront - Storage and Delivery

**Role:** Store generated assets, serve videos via CDN with low latency globally.

**Architecture:**

  * **S3 Buckets:**
      * `course-scripts/` - input text scripts, metadata JSON
      * `presenter-assets/` - photos, logos, branding
      * `generated-segments/` - individual video clips from APIs
      * `final-videos/` - assembled, production-ready course videos
  * **CloudFront Distribution:** CDN in front of S3 for fast global delivery
  * **Signed URLs:** Secure video access with expiration timestamps
  * **Lifecycle Policies:** Auto-archive old segments to Glacier after 30 days

**S3 + CloudFront Setup Example:**

```javascript
const AWS = require('aws-sdk');
const s3 = new AWS.S3();
const cloudfront = new AWS.CloudFront.Signer(
  process.env.CLOUDFRONT_KEY_PAIR_ID,
  process.env.CLOUDFRONT_PRIVATE_KEY
);

// Upload final video to S3
const uploadVideo = async (filePath, key) => {
  const fileStream = fs.createReadStream(filePath);
  await s3.upload({
    Bucket: 'your-course-videos',
    Key: key, // e.g., 'courses/ai-101/lesson-1.mp4'
    Body: fileStream,
    ContentType: 'video/mp4',
    ACL: 'private' // use signed URLs for access
  }).promise();
};

// Generate signed CloudFront URL (expires in 24 hours)
const getSignedUrl = (key) => {
  const url = `https://d1234abcd.cloudfront.net/${key}`;
  const policy = JSON.stringify({
    Statement: [{
      Resource: url,
      Condition: {
        DateLessThan: { 'AWS:EpochTime': Math.floor(Date.now()/1000) + 86400 }
      }
    }]
  });
  return cloudfront.getSignedUrl({ url, policy });
};
```

**Cost Estimates (US East):**

  * S3 storage: $0.023/GB/month (first 50TB)
  * S3 PUT requests: $0.005 per 1000 requests
  * CloudFront data transfer: $0.085/GB (first 10TB/month)
  * Typical 10-minute 1080p video: \~500MB, \~$0.01 storage + $0.04 transfer per view

-----

## Workflow Implementation

### End-to-End Course Generation Flow

**Input:** Course JSON specification

```json
{
  "course_id": "ai-fundamentals-101",
  "presenter": {
    "name": "Dr. Jane Smith",
    "photo_url": "https://storage.example.com/jane.jpg",
    "voice_id": "en-US-JennyNeural"
  },
  "branding": {
    "logo_url": "https://storage.example.com/logo.png",
    "primary_color": "#1E88E5",
    "secondary_color": "#FFC107"
  },
  "lessons": [
    {
      "lesson_id": "lesson-01",
      "title": "Introduction to AI",
      "script": "Welcome to AI Fundamentals. Today we explore...",
      "infographics": [
        {
          "type": "statistics",
          "data": { "heading": "AI Market Size", "value": "$2.4B" }
        }
      ],
      "broll": [
        { "prompt": "Modern data center servers", "duration": 8 }
      ]
    }
  ]
}
```

**Processing Steps:**

1.  **API Gateway receives request**
      * Validate JSON schema
      * Authenticate user, check quota
      * Generate unique job ID
      * Store request in PostgreSQL with status = 'pending'
      * Enqueue job to processing queue
      * Return job ID to client
2.  **Content Processing Engine**
      * Parse course JSON
      * Segment scripts into speaking blocks (max 2 min each for HeyGen)
      * Extract infographic requirements
      * Generate b-roll prompts from context
      * Create task list: [avatar\_segments, infographics, broll\_clips]
3.  **Parallel API Calls**
      * HeyGen: Generate all talking head segments
      * ContentDrips: Generate all infographics
      * WaveSpeedAI: Generate all b-roll clips
      * Each service returns job IDs; poll status until all complete
4.  **Download Generated Assets**
      * Fetch video URLs from HeyGen, WaveSpeedAI
      * Fetch image URLs from ContentDrips
      * Download all to `S3 generated-segments/` bucket
5.  **Animate Static Infographics (if needed)**
      * Use FFmpeg to create 5-8 sec video clips from PNG infographics
      * Add zoom/pan effects: `-vf "zoompan=z='zoom+0.002':d=250"`
      * Add fade in/out
6.  **Video Assembly**
      * Create FFmpeg concat list in correct order
      * Add transitions (crossfade, fade to black)
      * Normalize audio levels across segments
      * Add intro/outro if specified
      * Output final video to `S3 final-videos/` bucket
7.  **Post-Processing & Delivery**
      * Generate multiple resolutions (1080p, 720p, 480p) for adaptive streaming
      * Create thumbnail image (frame at 2 seconds)
      * Generate CloudFront signed URL with 7-day expiration
      * Update job status to 'completed' in database
      * Send webhook notification to client with video URL

-----

## Orchestration with Temporal.io

**Why Temporal:**

  * Durable workflow execution (survives crashes, retries)
  * Built-in retry policies and error handling
  * Workflow versioning and testing
  * Visibility: track each workflow step in UI
  * Language-agnostic (SDKs: Node.js, Python, Go, Java)

**Workflow Definition Example (TypeScript):**

```typescript
import { proxyActivities } from '@temporalio/workflow';
import type * as activities from './activities';

const {
  createAvatar,
  generateAvatarVideo,
  generateInfographic,
  generateBRoll,
  downloadAsset,
  assembleVideo,
  uploadToS3
} = proxyActivities<typeof activities>({
  startToCloseTimeout: '10 minutes',
  retry: { maximumAttempts: 3 }
});

export async function generateCourseWorkflow(input: CourseInput): Promise<string> {
  // Step 1: Create avatar (cached if already exists)
  const avatarId = await createAvatar({
    photoUrl: input.presenter.photo_url,
    name: input.presenter.name
  });

  // Step 2: Generate all video segments in parallel
  const segmentPromises = input.lessons.flatMap(lesson => [
    generateAvatarVideo({
      avatarId,
      script: lesson.script,
      voiceId: input.presenter.voice_id
    }),
    ...lesson.infographics.map(ig => generateInfographic({
      type: ig.type,
      data: ig.data,
      branding: input.branding
    })),
    ...lesson.broll.map(br => generateBRoll({
      prompt: br.prompt,
      duration: br.duration
    }))
  ]);
  const segments = await Promise.all(segmentPromises);

  // Step 3: Download all assets
  const localPaths = await Promise.all(
    segments.map(seg => downloadAsset(seg.url))
  );

  // Step 4: Assemble final video
  const finalVideoPath = await assembleVideo({
    segments: localPaths,
    transitions: 'fade',
    audioNormalize: true
  });

  // Step 5: Upload to S3 and get signed URL
  const videoUrl = await uploadToS3({
    filePath: finalVideoPath,
    bucket: 'final-videos',
    key: `courses/${input.course_id}/lesson-1.mp4`
  });

  return videoUrl;
}
```

**Activity Implementation Example:**

```typescript
// activities.ts
import fetch from 'node-fetch';

export async function generateAvatarVideo(params: {
  avatarId: string;
  script: string;
  voiceId: string;
}): Promise<{ url: string; duration: number }> {
  // Call HeyGen API
  const response = await fetch('https://api.heygen.com/v2/video/generate', {
    method: 'POST',
    headers: {
      'X-Api-Key': process.env.HEYGEN_API_KEY,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      video_inputs: [{
        character: { type: 'avatar', avatar_id: params.avatarId },
        voice: { type: 'text', input_text: params.script, voice_id: params.voiceId }
      }],
      dimension: { width: 1920, height: 1080 }
    })
  });
  const { video_id } = await response.json();

  // Poll until complete
  let status = 'processing';
  let videoUrl = '';
  while (status !== 'completed') {
    await new Promise(resolve => setTimeout(resolve, 5000)); // wait 5s
    const statusRes = await fetch(
      `https://api.heygen.com/v1/video.status?video_id=${video_id}`,
      { headers: { 'X-Api-Key': process.env.HEYGEN_API_KEY }}
    );
    const data = await statusRes.json();
    status = data.data.status;
    videoUrl = data.data.video_url;
    if (status === 'failed') throw new Error('Video generation failed');
  }
  return { url: videoUrl, duration: 120 }; // example
}
```

-----

## Infrastructure Setup

### Deployment Architecture

| Component | Deployment | Scaling |
| :--- | :--- | :--- |
| API Gateway | ECS Fargate or Lambda | Auto-scale by requests |
| Temporal Workers | ECS Fargate or EC2 | Horizontal pod autoscaling |
| FFmpeg Processing | EC2 with GPU or Lambda | On-demand spot instances |
| PostgreSQL | RDS PostgreSQL | Multi-AZ, read replicas |
| Redis Queue | ElastiCache Redis | Cluster mode |
| S3 + CloudFront | Managed services | Unlimited |

**Table 4: Infrastructure Components**

### Environment Variables

**API Keys**

  * `HEYGEN_API_KEY=hg_xxxxXXXXXXXXX`
  * `WAVESPEED_API_KEY=WS_XXXXXXXXXXXXX`
  * `CONTENTDRIPS_API_KEY=cd_xxxxxXXXXXXXX`

**AWS**

  * `AWS_REGION=us-east-1`
  * `S3_BUCKET_SEGMENTS=course-generated-segments`
  * `S3_BUCKET_FINAL=course-final-videos`
  * `CLOUDFRONT_DISTRIBUTION_ID=E1234ABCD`
  * `CLOUDFRONT_KEY_PAIR_ID=APKA1234567890`
  * `CLOUDFRONT_PRIVATE_KEY=/path/to/private-key.pem`

**Database**

  * `DATABASE_URL=postgresql://user:pass@rds-endpoint:5432/courses`

**Temporal**

  * `TEMPORAL_ADDRESS=temporal.example.com:7233`
  * `TEMPORAL_NAMESPACE=course-generation`

**Monitoring**

  * `DATADOG_API_KEY=dd_xXXXXXXXXXXXX`

### Docker Compose for Local Development

```yaml
version: '3.8'
services:
  api:
    build: ./api
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/courses
    volumes:
      - ./api:/app
    depends_on:
      - db
      - redis
  temporal:
    image: temporalio/auto-setup:latest
    ports:
      - "7233:7233"
      - "8088:8088"
    environment:
      - DB=postgresql
      - DB_PORT=5432
      - POSTGRES_USER=postgres
      - POSTGRES_PWD=postgres
      - POSTGRES_SEEDS=db
    depends_on:
      - db
  worker:
    build: ./worker
    environment:
      - TEMPORAL_ADDRESS=temporal:7233
      - HEYGEN_API_KEY=${HEYGEN_API_KEY}
      - WAVESPEED_API_KEY=${WAVESPEED_API_KEY}
      - CONTENTDRIPS_API_KEY=${CONTENTDRIPS_API_KEY}
    depends_on:
      - temporal
      - redis
  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: courses
    volumes:
      - postgres_data:/var/lib/postgresql/data
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
volumes:
  postgres_data:
```

-----

## Cost Estimation (Monthly)

**Scenario:** 100 course videos per month, 10 minutes each, 5 segments per video

| Service | Cost | Notes |
| :--- | :--- | :--- |
| HeyGen API (Scale) | $330 | 660 credits, ~$0.50/credit |
| WaveSpeedAI | $150 | \~1500 seconds b-roll @ $0.10/sec avg |
| ContentDrips API (Advanced) | $149 | \~500 infographics |
| AWS EC2 (FFmpeg workers) | $200 | 2x c5.2xlarge spot instances |
| AWS S3 Storage | $50 | \~2TB stored |
| AWS CloudFront | $300 | \~3TB data transfer |
| AWS RDS PostgreSQL | $100 | db.t3.medium multi-AZ |
| AWS ElastiCache Redis | $50 | cache.t3.micro |
| Temporal Cloud (optional) | $200 | Managed Temporal |
| Monitoring (Datadog) | $100 | APM + logs |
| **Total** | **$1,629/month\*\* | **\~$16.29 per 10-min video** |

**Table 5: Monthly Cost Breakdown**

**Cost Optimization Strategies:**

  * Use HeyGen Pay-as-you-go for sporadic usage (\<50 videos/month)
  * Switch to WaveSpeedAI Wan 2.2 model ($0.01/sec) for non-critical b-roll
  * Cache generated avatars and reuse across courses
  * Use S3 Intelligent-Tiering to auto-archive old videos
  * Leverage AWS Reserved Instances for predictable compute workloads
  * Batch process multiple courses to maximize API concurrency

-----

## Implementation Roadmap

### Phase 1: MVP (Weeks 1-4)

**Goal:** Proof-of-concept with single-lesson generation

  * **Week 1: API Integration**
      * Set up HeyGen, WaveSpeedAI, ContentDrips accounts
      * Test API endpoints manually (Postman/Insomnia)
      * Create test course JSON schema
      * Build simple Node.js script to call each API
  * **Week 2: Video Assembly**
      * Install FFmpeg locally
      * Download sample video segments from APIs
      * Write FFmpeg concatenation script
      * Test transitions, audio normalization
  * **Week 3: Storage & Delivery**
      * Set up AWS S3 buckets
      * Configure CloudFront distribution
      * Implement upload/download functions
      * Generate signed URLs for secure access
  * **Week 4: End-to-End Test**
      * Assemble all components into single workflow
      * Process one complete lesson start-to-finish
      * Measure timing: API calls, downloads, assembly
      * Document issues and optimizations needed

**Deliverables:**

  * Working prototype generating single-lesson video
  * API integration code (Node.js/Python)
  * FFmpeg assembly script
  * AWS S3 + CloudFront setup
  * Performance metrics document

### Phase 2: Orchestration & Scaling (Weeks 5-8)

**Goal:** Production-ready system with async processing

  * **Week 5: Job Queue & Database**
      * Set up PostgreSQL RDS instance
      * Design schema: courses, lessons, jobs, assets
      * Implement Redis queue with BullMQ
      * Create job enqueueing and status tracking
  * **Week 6: Temporal Workflows**
      * Install Temporal server (Docker or Temporal Cloud trial)
      * Convert prototype script into Temporal workflow
      * Implement activities for each API call
      * Add retry policies and error handling
  * **Week 7: API Gateway**
      * Build REST API with Express/FastAPI
      * Endpoints: POST /courses, GET /courses/:id/status, GET /videos/:id
      * Add authentication (JWT or API keys)
      * Rate limiting and quota management
  * **Week 8: Testing & Optimization**
      * Load testing with 10 concurrent course generations
      * Optimize API polling intervals
      * Implement caching for avatars and templates
      * Add monitoring with Datadog or CloudWatch

**Deliverables:**

  * Temporal workflows handling full course generation
  * REST API with documentation (OpenAPI/Swagger)
  * PostgreSQL database with migrations
  * Redis job queue processing
  * Monitoring dashboards

### Phase 3: Production Deployment (Weeks 9-12)

**Goal:** Deploy to AWS, productionize, add features

  * **Week 9: Infrastructure as Code**
      * Write Terraform or CloudFormation templates
      * Provision VPC, subnets, security groups
      * Deploy RDS, ElastiCache, S3, CloudFront
      * Set up ECS Fargate for API and workers
  * **Week 10: CI/CD Pipeline**
      * GitHub Actions or AWS CodePipeline
      * Automated testing (unit, integration)
      * Docker image builds and pushes to ECR
      * Blue-green deployment strategy
  * **Week 11: Advanced Features**
      * Multi-lesson course support
      * Custom transitions and branding per client
      * Adaptive streaming (HLS/DASH) via AWS MediaConvert
      * Webhook notifications for job completion
  * **Week 12: Launch & Documentation**
      * Finalize API documentation (Swagger UI)
      * Write developer guides and examples
      * Set up customer support channels
      * Soft launch with pilot customers

**Deliverables:**

  * Production infrastructure on AWS
  * CI/CD pipeline with automated deployments
  * Complete API documentation
  * Monitoring, alerting, logging setup
  * Onboarding materials for AI coding agents

-----

## API Specification

### Course Generation API

**Base URL:** `[https://api.yourservice.com/v1](https://api.yourservice.com/v1)`  
**Authentication:** Bearer token in Authorization header

#### POST /courses

**Description:** Create a new course generation job  
**Request Body:**

```json
{
  "course_id": "string (unique identifier)",
  "presenter": {
    "name": "string",
    "photo_url": "string (URL to presenter photo)",
    "voice_id": "string (e.g., en-US-JennyNeural)"
  },
  "branding": {
    "logo_url": "string (URL to logo)",
    "primary_color": "string (hex color)",
    "secondary_color": "string (hex color)"
  },
  "lessons": [
    {
      "lesson_id": "string",
      "title": "string",
      "script": "string (text to be spoken)",
      "infographics": [
        {
          "type": "statistics | comparison | timeline",
          "data": { /* custom data object */ }
        }
      ],
      "broll": [
        {
          "prompt": "string (description of scene)",
          "duration": 10
        }
      ]
    }
  ]
}
```

**Response (202 Accepted):**

```json
{
  "job_id": "job_abc123xyz",
  "status": "pending",
  "created_at": "2026-03-27T13:00:00Z",
  "estimated_completion": "2026-03-27T13:45:00Z"
}
```

#### GET /jobs/:job\_id

**Description:** Get status and details of a generation job  
**Response (200 OK):**

```json
{
  "job_id": "job_abc123xyz",
  "status": "processing | completed | failed",
  "progress": 65,
  "created_at": "2026-03-27T13:00:00Z",
  "updated_at": "2026-03-27T13:30:00Z",
  "videos": [
    {
      "lesson_id": "lesson-01",
      "video_url": "https://d1234.cloudfront.net/signed-url",
      "thumbnail_url": "https://d1234.cloudfront.net/thumb.jpg",
      "duration": 612,
      "size_bytes": 524288000
    }
  ],
  "error": null
}
```

#### GET /videos/:video\_id

**Description:** Get details and signed URL for a specific video  
**Response (200 OK):**

```json
{
  "video_id": "vid_xyz789",
  "course_id": "ai-fundamentals-101",
  "lesson_id": "lesson-01",
  "video_url": "https://d1234.cloudfront.net/signed-url",
  "expires_at": "2026-04-03T13:00:00Z",
  "formats": [
    {"resolution": "1080p", "url": "https://..." },
    {"resolution": "720p", "url": "https://..." },
    {"resolution": "480p", "url": "https://..." }
  ]
}
```

-----

## Security Considerations

  * **API Key Management**
      * Store all API keys in AWS Secrets Manager, not environment variables
      * Rotate keys every 90 days
      * Use separate keys for dev/staging/production
  * **Access Control**
      * Implement JWT authentication for API Gateway
      * Rate limiting: 100 requests/hour per user
      * Quota enforcement: track credits/usage per customer
  * **Video Delivery**
      * Use CloudFront signed URLs with expiration (24-hour default)
      * Optionally implement HMAC-based URL signing tied to user IP
      * Enable CloudFront access logs for audit trail
  * **Content Security**
      * Validate all input JSON against strict schemas (Joi/Zod)
      * Sanitize file uploads (presenter photos, logos)
      * Scan uploaded images for malware/exploits
      * Enforce content policies (no NSFW, copyrighted material)
  * **Data Privacy**
      * Encrypt all data at rest (S3 SSE, RDS encryption)
      * Encrypt data in transit (TLS 1.3 for all API calls)
      * Implement data retention policy: delete segments after 30 days
      * GDPR compliance: allow user data export and deletion

-----

## Monitoring & Observability

### Key Metrics to Track

| Metric | Target | Alert Threshold |
| :--- | :--- | :--- |
| API Response Time (p95) | \<500ms | \>1000ms |
| Video Generation Time | \<30min | \>60min |
| API Success Rate | \>99% | \<95% |
| FFmpeg Processing Time | \<5min | \>10min |
| S3 Upload Success Rate | \>99.9% | \<99% |
| CloudFront Cache Hit Rate | \>80% | \<70% |
| Temporal Workflow Failures | \<1% | \>5% |

**Table 6: SLA Metrics and Alerts**

### Logging Strategy

  * **Structured Logging:** JSON format with correlation IDs
  * **Log Aggregation:** AWS CloudWatch Logs or Datadog
  * **Log Levels:**
      * DEBUG: API request/response payloads (dev only)
      * INFO: Job status changes, workflow steps
      * WARN: API rate limits, retries, slow responses
      * ERROR: API failures, FFmpeg errors, upload failures
  * **Retention:** 30 days hot, 1 year cold storage (S3 Glacier)

### Alerting Rules

  * API error rate \>5% for 5 minutes → Page on-call engineer
  * HeyGen API quota \<10% remaining → Email admin
  * Video generation failed 3 times → Create incident ticket
  * S3 upload failures \>10 in 10 minutes → Investigate storage
  * Temporal workflow stuck \>2 hours → Auto-retry or manual intervention

-----

## Agent Handoff Checklist

### Prerequisites

  * AWS account with billing configured
  * HeyGen API account (Scale plan recommended for production)
  * WaveSpeedAI API account with credits
  * ContentDrips API account (Advanced or Pro plan)
  * Domain name for API (e.g., `api.coursevideos.com`)
  * SSL certificate (AWS ACM)
  * GitHub repository for code

### Step-by-Step Implementation Guide

1.  **Repository Setup**
      * Clone starter template: `git clone [https://github.com/your-repo/course-video-generator](https://github.com/your-repo/course-video-generator)`
      * Install dependencies: `npm install` or `pip install -r requirements.txt`
      * Copy `.env.example` to `.env` and fill in API keys
2.  **Local Development**
      * Run `docker-compose up` to start local services
      * Test HeyGen integration: `npm run test:heygen`
      * Test WaveSpeedAI integration: `npm run test:wavespeed`
      * Test ContentDrips integration: `npm run test:contentdrips`
      * Test FFmpeg assembly: `npm run test:ffmpeg`
3.  **AWS Infrastructure Setup**
      * `cd terraform/`
      * `terraform init`
      * `terraform plan -var-file=prod.tfvars`
      * `terraform apply -var-file=prod.tfvars`
      * Note outputs: S3 bucket names, RDS endpoint, Redis endpoint
4.  **Deploy Application**
      * Build Docker images: `docker build -t course-api:latest ./api`
      * Push to ECR: `aws ecr get-login-password | docker login ...`
      * Deploy to ECS: `aws ecs update-service --cluster course-cluster --service api`
      * Deploy Temporal workers: `aws ecs update-service --service workers`
5.  **Verification**
      * Health check: `curl [https://api.coursevideos.com/health](https://api.coursevideos.com/health)`
      * Create test course: `curl -X POST [https://api.coursevideos.com/v1/courses](https://api.coursevideos.com/v1/courses) -d @test-course.json`
      * Monitor job status: `curl [https://api.coursevideos.com/v1/jobs/](https://api.coursevideos.com/v1/jobs/){job_id}`
      * Download generated video and verify quality
6.  **Monitoring Setup**
      * Configure Datadog agent on ECS tasks
      * Import dashboards from `monitoring/dashboards/`
      * Set up alert rules from `monitoring/alerts/`
      * Test alert delivery (Slack, PagerDuty)

-----

## Common Troubleshooting

| Issue | Solution |
| :--- | :--- |
| HeyGen API returns 429 (rate limit) | Implement exponential backoff, upgrade to Scale plan |
| FFmpeg concat fails with codec error | Re-encode segments to same codec: -c:v libx264 -crf 23 |
| CloudFront returns 403 Forbidden | Check signed URL expiration, verify key pair ID |
| Temporal workflow stuck | Check worker logs, verify activities not timing out |
| Video quality is poor | Increase HeyGen resolution to 1080p, check bitrate settings |
| S3 upload times out | Increase timeout, use multipart upload for large files |

**Table 7: Common Issues and Solutions**

-----

## Future Enhancements

### Phase 4+ Roadmap

  * **Interactive Video Features**
      * Quizzes and polls embedded in videos (HeyGen interactive API)
      * Branching scenarios based on user choices
      * Clickable hotspots linking to resources
  * **Advanced Personalization**
      * Dynamic avatar selection based on audience demographics
      * Personalized intros with viewer name
      * A/B testing different presenter styles
  * **Multi-Language Support**
      * Automatic script translation (GPT-4, DeepL API)
      * Voice cloning in multiple languages (ElevenLabs Multilingual)
      * Subtitle generation and embedding (Whisper API)
  * **Analytics & Optimization**
      * Video engagement metrics (play rate, completion rate)
      * A/B test different infographic styles
      * Automatic re-generation based on performance data
  * **Content Management System**
      * Web UI for non-technical users to create courses
      * Template library for common course structures
      * Drag-and-drop lesson editor
      * Preview mode before final generation

-----

## Conclusion

This technical specification provides a complete blueprint for building a production-ready automated video course generation system. The architecture leverages best-in-class API services (HeyGen for lip-sync avatars, WaveSpeedAI for b-roll, ContentDrips for infographics), orchestrated via Temporal workflows, and deployed on AWS infrastructure.

**Key Success Factors:**

  * API-first design: Every component accessible programmatically
  * Modular architecture: Easy to swap services or add new features
  * Robust error handling: Retries, fallbacks, monitoring at every layer
  * Scalable infrastructure: Auto-scaling workers, CDN delivery, serverless where appropriate
  * Cost-conscious: Pay-per-use pricing, caching, resource optimization

**Next Steps:**

1.  Review this specification with your development team or AI coding agent
2.  Set up accounts with HeyGen, WaveSpeedAI, and ContentDrips
3.  Clone the starter repository and begin Phase 1 implementation
4.  Schedule weekly check-ins to track progress against roadmap
5.  Iterate based on early testing and user feedback

For questions or clarifications during implementation, refer to the official API documentation links provided in the References section below.

-----

## References

[1] HeyGen API Documentation. (2026). HeyGen Developer Portal. [https://docs.heygen.com](https://docs.heygen.com)  
[2] HeyGen. (2026). Create Photo Avatar - API Reference. [https://docs.heygen.com/reference/generate-photo-avatar-photos](https://docs.heygen.com/reference/generate-photo-avatar-photos)  
[3] HeyGen. (2026, March 22). HeyGen API Pricing Explained. [https://help.heygen.com/en/articles/10060327-heygen-api-pricing-explained](https://help.heygen.com/en/articles/10060327-heygen-api-pricing-explained)  
[4] Photonpay. (2026, March 24). HeyGen Pricing 2026: Complete Guide to Plans & Credits. [https://www.photonpay.com/hk/blog/article/heygen-pricing](https://www.photonpay.com/hk/blog/article/heygen-pricing)  
[5] WaveSpeedAI. (2026, March 3). Pricing - WaveSpeed. [https://wavespeed.ai/pricing](https://wavespeed.ai/pricing)  
[6] WaveSpeedAI. (2025, December 26). Complete Guide to AI Video Generation APIs in 2026. [https://wavespeed.ai/blog/posts/complete-guide-ai-video-apis-2026/](https://wavespeed.ai/blog/posts/complete-guide-ai-video-apis-2026/)  
[7] ContentDrips. (2026, March 17). Generate Social Media Graphics Programmatically | ContentDrips API. [https://contentdrips.com/api/](https://contentdrips.com/api/)  
[8] SocialRails. (2026, March 17). Contentdrips Pricing 2026: Plans, Costs & Value Analysis. [https://socialrails.com/blog/contentdrips-pricing](https://socialrails.com/blog/contentdrips-pricing)  
[9] Infogram. (2026). Infogram: Turn Data Into Interactive Stories. [https://infogram.com](https://infogram.com)  
[10] AWS. (2026, March 25). Tutorial: Hosting on-demand streaming video with Amazon S3, Amazon CloudFront, and Amazon Route 53. [https://docs.aws.amazon.com/AmazonS3/latest/userguide/tutorial-s3-cloudfront-route53-video-streaming.html](https://docs.aws.amazon.com/AmazonS3/latest/userguide/tutorial-s3-cloudfront-route53-video-streaming.html)  
[11] FFmpeg. (2025, August 30). Concatenate - FFmpeg. [https://trac.ffmpeg.org/wiki/Concatenate](https://trac.ffmpeg.org/wiki/Concatenate)  
[12] Mux. (2026). How to concatenate videos using ffmpeg. [https://www.mux.com/articles/stitch-multiple-videos-together-with-ffmpeg](https://www.mux.com/articles/stitch-multiple-videos-together-with-ffmpeg)
