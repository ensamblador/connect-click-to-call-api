import React, { useState } from 'react'
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import { Modal, Alert, Form, Button } from 'react-bootstrap';


const initialState = { name: '', phone: '' }
const modalInitialState = { title: '', message: '' }

const call_url = "https://fhkxjdlfcl.execute-api.us-east-1.amazonaws.com/prod/call_customer"


const mymodal = (title, message) =>

  <Modal.Dialog>
    <Modal.Header closeButton>
      <Modal.Title>{title}</Modal.Title>
    </Modal.Header>

    <Modal.Body>
      <p>{message}</p>
    </Modal.Body>

    <Modal.Footer>
      <Button variant="secondary">OK</Button>
    </Modal.Footer>
  </Modal.Dialog>

const App = () => {
  const [formState, setFormState] = useState(initialState)
  const [show, setShow] = useState(false);
  const [modalState, setModalState] = useState(modalInitialState);

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  const setInput = (key, value) => {
    setFormState({ ...formState, [key]: value })
  }

  const mymodal = () =>
    <Modal show={show} onHide={handleClose}>
      <Modal.Dialog>
        <Modal.Header closeButton>
          <Modal.Title>{modalState.title}</Modal.Title>
        </Modal.Header>

        <Modal.Body>
          <p>{modalState.message}</p>
        </Modal.Body>

        <Modal.Footer>
          <Button variant="secondary" onClick={handleClose}>OK</Button>
        </Modal.Footer>
      </Modal.Dialog>
    </Modal>


  const callMe = async (e) => {
    e.preventDefault()
    console.log('Call')
    try {
      if (!formState.name || !formState.phone) return

      const callData = { ...formState }
      setModalState({ title: 'Intentando Llamar', message: formState.name + ", pon atención al número " + formState.phone + ". Estamos llamando ahora..." })
      handleShow()
      console.log(callData)
      const callrequest = call_url + '?nombre=' + encodeURIComponent(formState.name) + '&telefono=' + encodeURIComponent(formState.phone)
      const response = fetch(callrequest, {
        method: 'GET'
      })
      await response
      console.log('data:', response)

      //console.log(response.json())
    } catch (err) { console.log('error calling', err) }
  }



  return (
    <div className="App">
      {mymodal()}
      <Alert variant="success">
        <Alert.Heading>Click to Call</Alert.Heading>
        <Form onSubmit={(e) => callMe(e)}>

          <Form.Group className="mb-3" controlId="formBasicEmail">
            <Form.Label>Nombre</Form.Label>
            <Form.Control
              type="text"
              placeholder="Ingrese su nombre"
              value={formState.name}
              onChange={event => setInput('name', event.target.value)}
            />

          </Form.Group>

          <Form.Group className="mb-3" controlId="formBasicPassword">
            <Form.Label>Teléfono</Form.Label>
            <Form.Control
              type="text"
              placeholder="+56912345678"
              value={formState.phone}
              onChange={event => setInput('phone', event.target.value)} />
          </Form.Group>
          <Button variant="primary" type="submit" >
            Llamar
          </Button>
        </Form>
      </Alert>
    </div>
  )
}


export default App;
