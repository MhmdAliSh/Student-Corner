import { useState } from 'react';
import { Link, NavLink, Route, Routes, useParams } from 'react-router-dom';
import { courses, student } from './data.js';

const pages = [
  ['Home', '/'],
  ['About', '/about'],
  ['Features', '/features'],
  ['Courses', '/courses'],
  ['Contact', '/contact'],
];

function App() {
  return (
    <div className="site">
      <header className="header">
        <Link className="logo" to="/">Student Corner</Link>
        <nav aria-label="Main navigation">
          {pages.map(([label, path]) => (
            <NavLink key={path} to={path} end={path === '/'}>
              {label}
            </NavLink>
          ))}
        </nav>
      </header>

      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/features" element={<Features />} />
          <Route path="/courses" element={<Courses />} />
          <Route path="/courses/:courseId" element={<CourseDetails />} />
          <Route path="/contact" element={<Contact />} />
          <Route path="*" element={<Home />} />
        </Routes>
      </main>

      <footer>Student Corner | CSCI426 project</footer>
    </div>
  );
}

function Home() {
  return (
    <>
      <section className="welcome">
        <p className="tag">STUDENT PORTAL</p>
        <h1>Welcome to Student Corner</h1>
        <p>View your courses and grades for this semester.</p>
        <Link className="button" to="/courses">View courses</Link>
      </section>

      <section className="content">
        <div className="section-heading">
          <h2>My courses</h2>
          <Link to="/courses">All courses</Link>
        </div>
        <div className="cards">
          {courses.slice(0, 3).map((course) => (
            <article className="card" key={course.id}>
              <span className="course-id">{course.id}</span>
              <h3>{course.title}</h3>
              <p className="instructor">Instructor: {course.instructor}</p>
              <Link to={`/courses/${encodeURIComponent(course.id)}`}>
                View course details
              </Link>
            </article>
          ))}
        </div>
      </section>
    </>
  );
}

function About() {
  return (
    <section className="content narrow">
      <p className="tag">ABOUT</p>
      <h1>About this project</h1>
      <p>
        Student Corner is a small student portal made for a university web
        programming project. It gives students a simple way to view course
        information.
      </p>
      <p>
        The website is built with React. The student and course details are
        example data and are not connected to a real university system.
      </p>
    </section>
  );
}

function Features() {
  return (
    <section className="content narrow">
      <p className="tag">FEATURES</p>
      <h1>Features</h1>
      <ul className="feature-list">
        <li>View the current course list.</li>
        <li>Open a course to see its instructor, credits, and grade.</li>
        <li>View a sample student profile.</li>
        <li>Try the contact form.</li>
      </ul>
      <h2>Student profile</h2>
      <div className="card profile">
        <p><b>Name:</b> {student.name}</p>
        <p><b>Major:</b> {student.major}</p>
        <p><b>Year:</b> {student.year}</p>
      </div>
    </section>
  );
}

function Courses() {
  return (
    <section className="content">
      <p className="tag">COURSES</p>
      <h1>My courses</h1>
      <p className="muted">Sample courses for the current semester.</p>
      <div className="cards">
        {courses.map((course) => (
          <article className="card" key={course.id}>
            <span className="course-id">{course.id}</span>
            <h2>{course.title}</h2>
            <p>{course.instructor}</p>
            <p>Grade: <b>{course.grade}</b></p>
            <Link to={`/courses/${encodeURIComponent(course.id)}`}>
              See details
            </Link>
          </article>
        ))}
      </div>
    </section>
  );
}

function CourseDetails() {
  const { courseId } = useParams();
  const course = courses.find((item) => item.id === courseId);

  if (!course) {
    return (
      <section className="content narrow">
        <h1>Course not found</h1>
        <Link to="/courses">Back to courses</Link>
      </section>
    );
  }

  return (
    <section className="content narrow">
      <p className="tag">COURSE DETAILS</p>
      <h1>{course.title}</h1>
      <div className="card">
        <p><b>Course code:</b> {course.id}</p>
        <p><b>Instructor:</b> {course.instructor}</p>
        <p><b>Credits:</b> {course.credits}</p>
        <p><b>Grade:</b> {course.grade}</p>
      </div>
      <p><Link to="/courses">Back to courses</Link></p>
    </section>
  );
}

function Contact() {
  const [sent, setSent] = useState(false);

  function handleSubmit(event) {
    event.preventDefault();
    setSent(true);
  }

  return (
    <section className="content narrow">
      <p className="tag">CONTACT</p>
      <h1>Contact us</h1>
      <p>Leave a message using the form below.</p>
      <form className="form" onSubmit={handleSubmit}>
        <label>
          Name
          <input required placeholder="Your name" />
        </label>
        <label>
          Email
          <input required type="email" placeholder="you@example.com" />
        </label>
        <label>
          Message
          <textarea required rows="5" placeholder="Write your message" />
        </label>
        <button className="button" type="submit">Send message</button>
        {sent && <p className="success">Message saved for this demo. No email was sent.</p>}
      </form>
    </section>
  );
}

export default App;
